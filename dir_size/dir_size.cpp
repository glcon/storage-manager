#include <windows.h>
#include <string>
#include <iostream>
#include <atomic>
#include <thread>
#include <vector>
#include <queue>
#include <mutex>
#include <condition_variable>
#include <exception>

class DirectoryQueue {
    std::queue<std::wstring> dirs;
    std::mutex mtx;
    std::condition_variable cv;
    bool finished = false;

public:
    void push(const std::wstring& dir) {
        {
            std::lock_guard<std::mutex> lock(mtx);
            dirs.push(dir);
        }
        cv.notify_one();
    }

    // Pop with wait, returns false if finished and queue empty
    bool pop(std::wstring& dir) {
        std::unique_lock<std::mutex> lock(mtx);
        cv.wait(lock, [this] { return !dirs.empty() || finished; });
        if (dirs.empty()) return false;
        dir = dirs.front();
        dirs.pop();
        return true;
    }

    void set_finished() {
        {
            std::lock_guard<std::mutex> lock(mtx);
            finished = true;
        }
        cv.notify_all();
    }

    bool is_empty() {
        std::lock_guard<std::mutex> lock(mtx);
        return dirs.empty();
    }
};

std::atomic<long long> total_size(0);

// Track how many directories are still pending to process
class TaskCounter {
    std::atomic<int> count;
    std::mutex mtx;
    std::condition_variable cv;

public:
    TaskCounter(int initial) : count(initial) {}

    void increment() {
        count.fetch_add(1, std::memory_order_relaxed);
    }

    void decrement() {
        int old = count.fetch_sub(1, std::memory_order_acq_rel);
        if (old == 1) {
            std::unique_lock<std::mutex> lock(mtx);
            cv.notify_all();
        }
    }

    void wait_for_zero() {
        std::unique_lock<std::mutex> lock(mtx);
        cv.wait(lock, [this] { return count.load(std::memory_order_acquire) == 0; });
    }
};

void scan_directory(DirectoryQueue& queue, TaskCounter& tasks) {
    try {
        std::wstring dir_path;
        while (queue.pop(dir_path)) {
            WIN32_FIND_DATAW find_data;
            std::wstring search_path = dir_path + L"\\*";

            HANDLE hFind = FindFirstFileExW(
                search_path.c_str(),
                FindExInfoBasic,
                &find_data,
                FindExSearchNameMatch,
                NULL,
                FIND_FIRST_EX_LARGE_FETCH
            );

            if (hFind == INVALID_HANDLE_VALUE) {
                // No files found or error, just decrement and continue
                tasks.decrement();
                continue;
            }

            do {
                const std::wstring name = find_data.cFileName;
                if (name == L"." || name == L"..")
                    continue;

                if (find_data.dwFileAttributes & FILE_ATTRIBUTE_REPARSE_POINT) {
                    continue; // skip symlinks/junctions
                }

                if (find_data.dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY) {
                    // New directory found, add it to queue and increment tasks
                    tasks.increment();
                    queue.push(dir_path + L"\\" + name);
                } else {
                    LARGE_INTEGER filesize;
                    filesize.HighPart = find_data.nFileSizeHigh;
                    filesize.LowPart = find_data.nFileSizeLow;
                    total_size += filesize.QuadPart;
                }
            } while (FindNextFileW(hFind, &find_data));

            FindClose(hFind);

            // Finished processing current directory
            tasks.decrement();
        }
    }
    catch (const std::exception& e) {
        // Optional: log error here
        tasks.decrement();
    }
    catch (...) {
        // Catch all
        tasks.decrement();
    }
}

extern "C" __declspec(dllexport)
long long get_directory_size(const wchar_t* path) {
    total_size = 0;

    DirectoryQueue queue;
    queue.push(path);

    // Initialize task counter with 1 (the initial directory)
    TaskCounter tasks(1);

    unsigned int num_threads = std::thread::hardware_concurrency();
    if (num_threads == 0) num_threads = 4;

    std::vector<std::thread> workers;
    for (unsigned int i = 0; i < num_threads; ++i) {
        workers.emplace_back(scan_directory, std::ref(queue), std::ref(tasks));
    }

    // Wait until all directories processed
    tasks.wait_for_zero();

    // Signal the queue that no more directories will be added
    queue.set_finished();

    for (auto& t : workers) {
        if (t.joinable()) {
            t.join();
        }
    }

    return total_size.load();
}