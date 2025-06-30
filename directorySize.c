#include <stdio.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <dirent.h>
#include <string.h>

long long get_dir_size(const char *path) {
    DIR *dir = opendir(path);
    if (!dir) return 0;  // skip on error

    struct dirent *entry;
    long long total = 0;
    struct stat st;
    char fullpath[4096];

    while ((entry = readdir(dir)) != NULL) {
        if (!strcmp(entry->d_name, ".") || !strcmp(entry->d_name, ".."))
            continue;

        snprintf(fullpath, sizeof(fullpath), "%s/%s", path, entry->d_name);
        if (stat(fullpath, &st) == -1)
            continue;  // skip on error

        if (S_ISDIR(st.st_mode)) {
            total += get_dir_size(fullpath);
        } else {
            total += st.st_size;
        }
    }
    closedir(dir);
    return total;
}

int main(int argc, char *argv[]) {
    if (argc != 2) return 1;

    long long size = get_dir_size(argv[1]);
    printf("%lld", size);
    return 0;
}