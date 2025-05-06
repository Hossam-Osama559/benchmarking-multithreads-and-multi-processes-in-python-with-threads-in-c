#include <winsock2.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <windows.h>

#define MAX_CLIENTS 10
#define PORT 5000
#define SPACE 5
#define WIN_POSITION 30
#define SPEED 1000000000

int thread_cursor_pos[MAX_CLIENTS] = {0};
int game_over = 0;
int winner = 0;
int thread_id = 0;
HANDLE threadHandles[MAX_CLIENTS];

void move_cursor(int x, int y) {
    COORD coord;
    coord.X = x;
    coord.Y = y;
    SetConsoleCursorPosition(GetStdHandle(STD_OUTPUT_HANDLE), coord);
}

void clear_screen() {
    system("cls");
}

void print_vertical(int x, int y_start, const char* text) {
    for (int i = 0; text[i] != '\0'; i++) {
        move_cursor(x, y_start + i);  
        printf("%c", text[i]);
        fflush(stdout);
    }
}




void check_winner() {
    while (!game_over) {
        for (int i = 0; i < MAX_CLIENTS; i++) {
            if (thread_cursor_pos[i] == WIN_POSITION) {
                winner = i;
                game_over = 1;
                break;
            }
        }
    }
}




DWORD WINAPI handle_client_connection(LPVOID param) {
    SOCKET client_socket = *(SOCKET*)param;
    int x = thread_id++;
    
    while (!game_over) {
        print_vertical(x * SPACE, thread_cursor_pos[x], "|");
        thread_cursor_pos[x]++;


        for (int i =0;i<SPEED;i++){
           
            continue;
        }
    }


    closesocket(client_socket);
    return 0;
}

SOCKET setup_server() {
    WSADATA wsaData;
    SOCKET server_socket;
    struct sockaddr_in server_addr;

    if (WSAStartup(MAKEWORD(2, 2), &wsaData) != 0) {
        printf("WSAStartup failed\n");
        exit(1);
    }

    server_socket = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
    if (server_socket == INVALID_SOCKET) {
        printf("Socket creation failed\n");
        WSACleanup();
        exit(1);
    }

    memset(&server_addr, 0, sizeof(server_addr));
    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = INADDR_ANY;
    server_addr.sin_port = htons(PORT);

    if (bind(server_socket, (struct sockaddr*)&server_addr, sizeof(server_addr)) == SOCKET_ERROR) {
        printf("Bind failed\n");
        closesocket(server_socket);
        WSACleanup();
        exit(1);
    }

    if (listen(server_socket, MAX_CLIENTS) == SOCKET_ERROR) {
        printf("Listen failed\n");
        closesocket(server_socket);
        WSACleanup();
        exit(1);
    }

    // Set the server socket to non-blocking mode
    u_long mode = 1;  // Non-blocking mode
    if (ioctlsocket(server_socket, FIONBIO, &mode) != NO_ERROR) {
        printf("ioctlsocket failed\n");
        closesocket(server_socket);
        WSACleanup();
        exit(1);
    }

    return server_socket;
}

SOCKET accept_with_timeout(SOCKET server_socket, int timeout_sec) {
    fd_set readfds;
    struct timeval timeout;
    SOCKET client_socket;

    timeout.tv_sec = timeout_sec;
    timeout.tv_usec = 0;

    FD_ZERO(&readfds);
    FD_SET(server_socket, &readfds);

    int result = select(0, &readfds, NULL, NULL, &timeout);

    if (result > 0) {
        client_socket = accept(server_socket, NULL, NULL);
        if (client_socket == INVALID_SOCKET) {
            printf("Accept failed\n");
            return INVALID_SOCKET;
        }
        return client_socket;
    } else if (result == 0) {
       
        return INVALID_SOCKET;
    } else {
        printf("select failed with error: %d\n", WSAGetLastError());
        return INVALID_SOCKET;
    }
}

int main() {

    LARGE_INTEGER frequency;
    LARGE_INTEGER start, end;
    double elapsed;

    QueryPerformanceFrequency(&frequency);


    QueryPerformanceCounter(&start);


    SOCKET server_socket, client_socket;
    struct sockaddr_in client_addr;
    int client_len = sizeof(client_addr);

    
    server_socket = setup_server();

    // Start the winner checking thread
    CreateThread(NULL, 0, (LPTHREAD_START_ROUTINE)check_winner, NULL, 0, NULL);

    // Clear the screen
    clear_screen();

    // Accept client connections with timeout
    while (!game_over) {
        client_socket = accept_with_timeout(server_socket, 1);  // 1 second timeout
        if (client_socket != INVALID_SOCKET) {
            // Create a new thread to handle the client
            CreateThread(NULL, 0, handle_client_connection, (LPVOID)&client_socket, 0, NULL);
        }
    }

    // Print the winner after game over
    move_cursor(0, 40);  // Move the cursor to position (0, 40)
    printf("Here is the champ: Thread %d\n", winner);

    // Clean up
    closesocket(server_socket);
    WSACleanup();



    QueryPerformanceCounter(&end);


    elapsed = (double)(end.QuadPart - start.QuadPart) / frequency.QuadPart;



    printf("time takes is %.6f",elapsed);

    return 0;
}
