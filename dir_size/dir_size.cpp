#include <windows.h>
#include <string>
#include <iostream>
#include <atomic>
#include <thread>
#include <vector>
#include <queue>
#include <mutex>
#include <condition_variable>

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

void scan_directory(DirectoryQueue& queue) {
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
                std::wstring subdir = dir_path + L"\\" + name;
                queue.push(subdir);
            } else {
                LARGE_INTEGER filesize;
                filesize.HighPart = find_data.nFileSizeHigh;
                filesize.LowPart = find_data.nFileSizeLow;
                total_size += filesize.QuadPart;
            }
        } while (FindNextFileW(hFind, &find_data));

        FindClose(hFind);
    }
}

int wmain(int argc, wchar_t* argv[]) {
    if (argc != 2) {
        std::wcerr << L"Usage: size.exe <directory_path>\n";
        return 1;
    }

    DirectoryQueue queue;
    queue.push(argv[1]);

    const unsigned int num_threads = std::thread::hardware_concurrency();
    std::vector<std::thread> workers;

    for (unsigned int i = 0; i < num_threads; ++i) {
        workers.emplace_back(scan_directory, std::ref(queue));
    }

    while (true) {
        if (queue.is_empty()) {
            queue.set_finished();
            break;
        }
        Sleep(100);
    }

    for (auto& t : workers) {
        t.join();
    }

    std::wcout << total_size.load() << std::endl;
    return 0;
}