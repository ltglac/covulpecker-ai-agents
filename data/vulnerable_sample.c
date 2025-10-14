// Sample vulnerable C code - Buffer Overflow
// This file contains intentional security vulnerabilities for testing

#include <stdio.h>
#include <string.h>
#include <stdlib.h>

// Vulnerability 1: Classic buffer overflow with strcpy
void buffer_overflow_strcpy(char *input) {
    char buffer[64];
    strcpy(buffer, input);  // No bounds checking!
    printf("Data: %s\n", buffer);
}

// Vulnerability 2: gets() - deprecated and dangerous
void dangerous_gets() {
    char username[32];
    printf("Enter username: ");
    gets(username);  // Extremely dangerous - no bounds checking
    printf("Welcome, %s!\n", username);
}

// Vulnerability 3: Format string vulnerability
void format_string_bug(char *user_input) {
    printf(user_input);  // Should be printf("%s", user_input)
}

// Vulnerability 4: Integer overflow leading to buffer overflow
void integer_overflow(unsigned int size, char *data) {
    char *buffer;
    unsigned int total_size = size + 10;  // Can overflow!
    buffer = (char *)malloc(total_size);
    
    if (buffer) {
        memcpy(buffer, data, size);
        free(buffer);
    }
}

// Vulnerability 5: Use after free
void use_after_free() {
    char *ptr = (char *)malloc(100);
    free(ptr);
    strcpy(ptr, "Still using freed memory!");  // Use after free
    printf("%s\n", ptr);
}

// Vulnerability 6: Memory leak
void memory_leak(int count) {
    for (int i = 0; i < count; i++) {
        char *data = (char *)malloc(1024);
        // Forgot to free!
    }
}

int main(int argc, char *argv[]) {
    if (argc > 1) {
        buffer_overflow_strcpy(argv[1]);
    }
    
    return 0;
}
