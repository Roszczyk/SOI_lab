#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

typedef enum Month{JANUARY=1, FEBRUARY, MARCH, APRIL, MAY, JUNE, JULY, AUGUST, SEPTEMBER, OCTOBER, NOVEMBER, DECEMBER} Month;
typedef enum isDir{FILE, DIRECTORY} IsDir;

const int size_of_block = 1000000;

typedef struct Date{
	uint8_t day;
	Month month;
	uint16_t year;
} Date;

typedef struct Superblok{
	uint16_t disc_size;
	uint16_t block_size;
	uint16_t usage;
	uint8_t number_of_files;
	uint8_t free_blocks;
	Date modification;
} Superblok;

typedef struct iNode{
	Date created;
	Date modified;
	char permissions[3]; // rwx
	uint16_t data_blocks_refs[10];
	uint16_t file_size;
	IsDir isDir;
	uint8_t references;
	uint16_t references_table[10];
} iNode;

typedef struct metadata{
	Superblok superblok;
	iNode table[10];
} Metadata;

typedef struct FileBlock{
	char nazwa[15];
	char zawartosc[size_of_block];
} FileBlock;

typedef struct DirectoryBlock{
	char nazwa[15];
	uint16_t files_size;
	uint16_t podkatalogi_refs[100];
	uint16_t pliki_refs[100];
} DirectoryBlock;

typedef struct HardLink {
	char nazwa[15];
	uint16_t ref[10];
} HardLink;

int findEmptyBlock(void)
{
	int position;
	// do napisania
	return position;
}

int findEmptyINode(void)
{
	int position;
	// do napisania
	return position;
}

void addToINode(int number, int ref)
{
	// do napisania
}

void addToDisk(char**buffer)
{
	FileBlock new;
	//do napisania
}

void importFile(char ** fileName, FILE* disk)
{
	FILE * f;
	f = fopen(fileName, "rb");
	int length=fseek(f, 0L, SEEK_END)+1;	//znalezienie długości pliku
	fseek(f, 0L, SEEK_SET);					//powrót kursora do początku
	int numOfBlocksNeeded = length/size_of_block + length%size_of_block;
	int iNodeNum=findEmptyINode();
	int position;
	char buffer[size_of_block];
	for(int i=0; i<numOfBlocksNeeded; i++)
	{
		position=findEmptyBlock();
		fread(buffer, size_of_block, 1, f);
		addToDisk(buffer);
		addToINode(iNodeNum, position);
	}
}

int command_interpreter(char * command){
	if (strcmp(command, "import")){
		return 1;
	}
	if (strcmp(command, "export")){
		return 2;
	}
	return -1;
}

int main(int argc, char**argv){
	FILE * file;
	int task = command_interpreter(argv[2]);
	if (task==-1){
		printf("Error - task not known");
		return 1;
	}
	if (task==1){
		file = fopen(argv[1], "wb");
	}		
}
