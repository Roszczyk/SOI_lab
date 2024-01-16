#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

typedef enum Month{JANUARY=1, FEBRUARY, MARCH, APRIL, MAY, JUNE, JULY, AUGUST, SEPTEMBER, OCTOBER, NOVEMBER, DECEMBER} Month;
typedef enum isDir{FILE, DIRECTORY} IsDir;

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
	uint16_t data_blocks;
	uint16_t file_size;
	IsDir isDir;
	uint8_t references;
} iNode;

typedef struct metadata{
	Superblok superblok;
	iNode table[10];
}

