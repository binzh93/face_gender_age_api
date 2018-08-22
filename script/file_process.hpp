// #include <stdio.h>
#include <stdlib.h>
#include<string>
#include<dirent.h>
#include<iostream>
#include <vector>
// #include "dataInput.hpp"

// #include <unistd.h>
// #include <dirent.h>

// char img_path[500][1000];
// int img_num=0;
using namespace std;
// using std::vector;
// struct dirent
// {
//    long d_ino; /* inode number 索引节点号 */
//    off_t d_off; /* offset to this dirent 在目录文件中的偏移 */
//    unsigned short d_reclen; /* length of this d_name 文件名长 */
//    unsigned char d_type; /* the type of d_name 文件类型 */
//    char d_name [NAME_MAX+1]; /* file name (null-terminated) 文件名，最长255字符 */
// }



bool endswith(const char *str, const char *end){
    bool result = false;
    if ((str != NULL) && (end != NULL) ){
        int l1 = strlen(str);
        int l2 = strlen(end);
        if(l1>=l2){
            if(strcmp(str+l1-l2, end)==0){
                result = true;
            }
        }
    }
    return result;
}


bool startswith(const char *str, const char *start){
    bool result = false;
    if ((str != NULL) && (start != NULL) ){
        int l1 = strlen(str);
        int l2 = strlen(start);
        if(l1 >= l2){
            for(int i=0; i<l2; i++){
                if (str[i]==start[i]){
                    result = true;
                }else{
                    result = false;
                    break;
                }
            }
        }
    }
    return result;
}


vector<char*> readFileList(const char *basePath)
{
    //vector<string> score = {};
    // vector<stirng> s ={};
    vector<char*> poseJsonList;

    DIR *dir;
    struct dirent *ptr;
    char base[1000];
    char *picPath;
//     const char *start = "pose";
//     const char *end = ".json";

    if ((dir=opendir(basePath)) == NULL)
    {
        perror("Open dir error...");
        exit(1);
    }

    while ((ptr=readdir(dir)) != NULL)
    {
        if(strcmp(ptr->d_name,".")==0 || strcmp(ptr->d_name,"..")==0)    ///current dir OR parrent dir
            continue;
        else if(ptr->d_type == 8){    ///file
            // printf("d_name:%s/%s\n", basePath, ptr->d_name);
            // cout << "1" << endl;
            if(startswith(ptr->d_name, "pose") && endswith(ptr->d_name, ".json")){
                picPath = new char[1000];
                strcpy(picPath, basePath);
                strcat(picPath, "/");
                strcat(picPath, ptr->d_name);
                poseJsonList.push_back(picPath);
            }
        }    
        else if(ptr->d_type == 10){    ///link file
            // printf("d_name:%s/%s\n", basePath, ptr->d_name);
            // cout << "2" << endl;
            if(startswith(ptr->d_name, "pose") && endswith(ptr->d_name, ".json")){
                picPath = new char[1000];
                strcpy(picPath, basePath);
                strcpy(picPath, "/");
                strcpy(picPath, ptr->d_name);
                poseJsonList.push_back(picPath);
            }
        } 
        else if(ptr->d_type == 4)    ///dir
        {
            cout << "3" << endl;
            memset(base,'\0',sizeof(base));
            strcpy(base,basePath);
            strcat(base,"/");
            strcat(base,ptr->d_name);
            readFileList(base);
        }
    }
    closedir(dir);
    return poseJsonList;
}








// int main()
// {
//     // printf("Enter Image Path: ");
//     // fflush(stdout);
//     // char basePath[100]="data/";
//     // input=fgets(input, 256, stdin);
//     // if(!input) return;
//     // strtok(input, "\n");
//     // strcat(basePath,input);
//     // strcat(basePath,"/");

//     const char* basePath = "/Users/bin/Desktop/icrawler的副本/docs";
//     vector<char *> poseJsonList = readFileList(basePath);
//     // cout << poseJsonList.size() << endl;
//     for(size_t i=0; i < poseJsonList.size(); i++){
//         cout << poseJsonList[i] << endl;
//     }

//     // bool sd = startswith("posdsad", "pose");
//     // bool sd = endswith("dsada.json", "ljson");
//     // cout << sd << endl;
//     return 0;
// }


// int main(){
//     char * a1 = "dadas.json";
//     //const char * a1 = "dadas.json";
//     bool flag = endswith(a1, ".json");
//     cout << flag << endl;
//     return 0;

// }




// struct _finddata_t
// {
//     unsigned attrib;
//     time_t time_create;
//     time_t time_access;
//     time_t time_write;
//     _fsize_t size;
//     char name[_MAX_FNAME];
// };

// void getAllFiles( string path, vector<string>& files) 
// { 
//   //文件句柄 
//   long  hFile  =  0; 
//   //文件信息 
//   struct _finddata_t fileinfo; 
//   string p; 
//   if((hFile = _findfirst(p.assign(path).append("\\*").c_str(),&fileinfo)) != -1) 
//   { 
//     do
//     {  
//       if((fileinfo.attrib & _A_SUBDIR)) 
//       { 
//         if(strcmp(fileinfo.name,".") != 0 && strcmp(fileinfo.name,"..") != 0) 
//         {
//          files.push_back(p.assign(path).append("\\").append(fileinfo.name) );
//           getFilesall( p.assign(path).append("\\").append(fileinfo.name), files ); 
//         }
//       } 
//       else
//       { 
//         files.push_back(p.assign(path).append("\\").append(fileinfo.name) ); 
//       } 
//     }while(_findnext(hFile, &fileinfo) == 0); 
//     _findclose(hFile); 
//   } 
// }