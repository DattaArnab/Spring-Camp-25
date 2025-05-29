#include <stdio.h>
#include <string.h>
#include <assert.h>

#include <unistd.h>
#include <sys/stat.h>

#include "pclubgit.h"
#include "util.h"

/* Implementation Notes:
 *
 * - Functions return 0 if successful, 1 if there is an error.
 * - All error conditions in the function description need to be implemented
 *   and written to stderr. We catch some additional errors for you in main.c.
 * - Output to stdout needs to be exactly as specified in the function description.
 * - Only edit this file (pclubgit.c)
 * - You are given the following helper functions:
 *   * fs_mkdir(dirname): create directory <dirname>
 *   * fs_rm(filename): delete file <filename>
 *   * fs_mv(src,dst): move file <src> to <dst>, overwriting <dst> if it exists
 *   * fs_cp(src,dst): copy file <src> to <dst>, overwriting <dst> if it exists
 *   * write_string_to_file(filename,str): write <str> to filename (overwriting contents)
 *   * read_string_from_file(filename,str,size): read a string of at most <size> (incl.
 *     NULL character) from file <filename> and store it into <str>. Note that <str>
 *     needs to be large enough to hold that string.
 */

/* pclubgit init
 *
 * - Create .pclubgit directory
 * - Create empty .pclubgit/.index file
 * - Create .pclubgit/.prev file containing 0..0 commit id
 *
 * Output (to stdout):
 * - None if successful
 */

int pclubgit_init(void) {
  fs_mkdir(".pclubgit");

  FILE* findex = fopen(".pclubgit/.index", "w");
  fclose(findex);
  
  write_string_to_file(".pclubgit/.prev", "0000000000000000000000000000000000000000");

  return 0;
}


/* pclubgit add <filename>
 * 
 * - Append filename to list in .pclubgit/.index if it isn't in there yet
 *
 * Possible errors (to stderr):
 * >> ERROR: File <filename> already added
 *
 * Output (to stdout):
 * - None if successful
 */

int pclubgit_add(const char* filename) {
  FILE* findex = fopen(".pclubgit/.index", "r");
  FILE* fnewindex = fopen(".pclubgit/.newindex", "w");

  char line[FILENAME_SIZE];

  while(fgets(line, sizeof(line), findex)) {
    strtok(line, "\n");
    if (strcmp(line, filename) == 0) {
      fprintf(stderr, "ERROR: File %s already added\n", filename);
      fclose(findex);
      fclose(fnewindex);
      fs_rm(".pclubgit/.newindex");
      return 3;
    }
    fprintf(fnewindex, "%s\n", line);
  }

  fprintf(fnewindex, "%s\n", filename);
  fclose(findex);
  fclose(fnewindex);

  fs_mv(".pclubgit/.newindex", ".pclubgit/.index");

  return 0;
}


/* pclubgit rm <filename>
 * 
 * See "Step 2" in the homework 1 spec.
 *
 */

int pclubgit_rm(const char* filename) {
  /* COMPLETE THE REST */
  FILE* findex = fopen(".pclubgit/.index", "r");
  FILE* fnewindex = fopen(".pclubgit/.newindex", "w");

  char line[FILENAME_SIZE];
  int tracked = 0;

  while(fgets(line, sizeof(line), findex)){
    strtok(line, "\n");

    if(strcmp(line, filename) == 0){
      tracked = 1;
    }
    else{
      fprintf(fnewindex, "%s\n", line);
    }
  }

  if(!tracked){
    fprintf(stderr, "ERROR: File %s not tracked\n", filename);
    fs_rm(".pclubgit/.newindex");

    fclose(findex);
    fclose(fnewindex);
    return 1;
  }

  fs_mv(".pclubgit/.newindex", ".pclubgit/.index");
  fclose(findex);
  fclose(fnewindex);

  return 0;
}

/* pclubgit commit -m <msg>
 *
 * See "Step 3" in the homework 1 spec.
 *
 */

const char* go_pclub = "GO PCLUB!";

int is_commit_msg_ok(const char* msg) {
  /* COMPLETE THE REST */
  return strstr(msg, go_pclub) != NULL;
}

void next_commit_id(char* commit_id) {
  /* COMPLETE THE REST */

  //'1' -> 0, '6' -> 1, 'c' -> 2 in ternary

  //if commit id is "cc...c" (largest possible ID) then "11...1" (lowest possible ID) will be returned.

  /*If no commit has been made yet then the commit id is all 0s.
  * In that case, set the commit id to the smallest possible one.
  */
  if(strcmp(commit_id, "0000000000000000000000000000000000000000") == 0){
    strcpy(commit_id, "1111111111111111111111111111111111111111");
    return;
  }

  // printf("commit id is: %s\n commit size is %zu\n", commit_id, strlen(commit_id)); //For debugging
  assert(strlen(commit_id) == COMMIT_ID_BYTES);

  //Essentially, adding 1 to the ternary representation
  for (int i = COMMIT_ID_BYTES-1; i >= 0; --i)
  {
    if(commit_id[i] == 'c'){
      commit_id[i] = '1';
    }
    else if(commit_id[i] == '6'){
      commit_id[i] = 'c';
      break;
    }
    else{ //commit_id[i] == '1'
      commit_id[i] = '6';
      break;
    }
  }
  // printf("New commit id is %s\n", commit_id); //For debugging
}

int pclubgit_commit(const char* msg) {
  if (!is_commit_msg_ok(msg)) {
    fprintf(stderr, "ERROR: Message must contain \"%s\"\n", go_pclub);
    return 1;
  }

  char commit_id[COMMIT_ID_SIZE] = {0};
  read_string_from_file(".pclubgit/.prev", commit_id, COMMIT_ID_BYTES);

  next_commit_id(commit_id);

  /* COMPLETE THE REST */

  //Make a directory with name .pclubgit/<new_id>
  char dir_name[FILENAME_SIZE] = ".pclubgit/";
  strcat(dir_name, commit_id);

  fs_mkdir(dir_name);

  //copy .index file into new directory
  char index_path[FILENAME_SIZE];
  strcpy(index_path, dir_name);
  strcat(index_path, "/.index");

  fs_cp(".pclubgit/.index", index_path);

  //copy .prev into new directory
  char prev_path[FILENAME_SIZE];
  strcpy(prev_path, dir_name);
  strcat(prev_path, "/.prev");

  fs_cp(".pclubgit/.prev", prev_path);

  //make a .msg file in the new directory
  char msg_path[FILENAME_SIZE];
  strcpy(msg_path, dir_name);
  strcat(msg_path, "/.msg");

  //write the commit message to the .msg file
  FILE* fmsg = fopen(msg_path, "w");
  fprintf(fmsg, "%s\n", msg);
  fclose(fmsg);

  //write the new ID into the main .prev file
  FILE* fprev = fopen(".pclubgit/.prev", "w");
  fprintf(fprev, "%s", commit_id);
  fclose(fprev);

  //TODO: Copy all tracked files
  FILE* findex = fopen(".pclubgit/.index", "r");
  //
  char line[FILENAME_SIZE];

  //fgets reads the newline character too
  while(fgets(line, sizeof(line), findex)){
    strtok(line, "\n"); //remove newline char from the end of the line

    //Path of the new file: .pclubgit/<commit_id>/file_name
    char file_path[FILENAME_SIZE];
    strcpy(file_path, dir_name);
    strcat(file_path, "/");
    strcat(file_path, line);

    fs_cp(line, file_path);
  }
  fclose(findex);

  return 0;
}

/* pclubgit status
 *
 * See "Step 1" in the homework 1 spec.
 *
 */

int pclubgit_status() {
  /* COMPLETE THE REST */
  FILE* findex = fopen(".pclubgit/.index", "r");

  char line[FILENAME_SIZE];
  size_t num = 0;

  printf("Tracked files:\n\n");

  //fgets reads the newline character too
  while(fgets(line, sizeof(line), findex)){
    num++;
    printf("%s", line);
  }
  
  printf("\n%zu file(s) total\n", num);
  fclose(findex);

  return 0;
}

/* pclubgit log
 *
 * See "Step 4" in the homework 1 spec.
 *
 */

int pclubgit_log() {
  /* COMPLETE THE REST */
  char commit_id[COMMIT_ID_SIZE] = {0};
  read_string_from_file(".pclubgit/.prev", commit_id, COMMIT_ID_BYTES);

  if(0 == strcmp(commit_id, "0000000000000000000000000000000000000000")){
    fprintf(stderr, "ERROR: There are no commits!\n");
    return 1;
  }

  // printf("DEBUG: commit id in .prev is %s\n", commit_id);

  while(0 != strcmp(commit_id, "0000000000000000000000000000000000000000")){
    //print commit messages

    char dir_path[FILENAME_SIZE] = ".pclubgit/";
    strcat(dir_path, commit_id); //.pclubgit/<commit_id>
    
    char msg_path[FILENAME_SIZE];
    strcpy(msg_path, dir_path); //.pclubgit/<commit_id>
    strcat(msg_path, "/.msg");

    // printf("DEBUG: message path is %s\n", msg_path);

    char commit_msg[MSG_SIZE] = {0};
    read_string_from_file(msg_path, commit_msg, MSG_SIZE-1);

    printf("commit %s %s", commit_id, commit_msg);

    char prev_path[FILENAME_SIZE];
    strcpy(prev_path, dir_path);
    strcat(prev_path, "/.prev"); //.pclubgit/<commit_id>/.prev

    // printf("DEBUG: path of .prev is %s\n", prev_path);

    //switch to previous commit
    read_string_from_file(prev_path, commit_id, COMMIT_ID_BYTES);
  }

  return 0;
}
