#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "dos2unicode.h"

void dump_char(char* font, int c)
{
	char* start = font + c * 16;
	char filename[] = "X.pbm";

	char line[8+1];

	filename[0] = c;
	FILE* dump = fopen(filename, "wt");

	fprintf(dump, "P1\n");
	fprintf(dump, "8 16\n");

	for (int i = 0; i < 16; ++i)
	{
		memset(line, 0, 8+1);

		for (int j = 0; j < 8; ++j)
		{
			if((start[i] & ( 1 << j )) >> j)
				line[7-j] = '*';
			else
				line[7-j] = ' ';
		}

		printf(dump, "%s\n", line);
	}

	fclose(dump);
}

#include <ctype.h>

void strlwr(char *s){
    char *ptr = s;
    while(*ptr != '\0'){
        *ptr = tolower(*ptr);
        ptr++;
    }
}

int main(int argc, char* argv[])
{
	char fontname[256];
	char bdfname[256];

	FILE* src = fopen(argv[1], "rb");

	int n = 4096;

	char* data = (char*)malloc(n);

	fread(data, n, 1, src);

	fclose(src);

	strcpy(fontname, argv[1]);
	strlwr(fontname);

	char* dot = strchr(fontname, '.');
	*dot = 0;

	printf("font name = %s\n", fontname);

	strcpy(bdfname, fontname);
	strcat(bdfname, ".bdf");

	FILE* bdf = fopen(bdfname, "wt");

/*
	fprintf(bdf, "STARTFONT 2.1\n");
	fprintf(bdf, "FONT -gnu-%s-medium-r-normal--16-160-75-75-c-80-iso10646-1\n", fontname);
	fprintf(bdf, "SIZE 16 75 75\n");
	fprintf(bdf, "FONTBOUNDINGBOX 8 16 0 -2\n");
	fprintf(bdf, "STARTPROPERTIES 2\n");
	fprintf(bdf, "FONT_ASCENT 14\n");
	fprintf(bdf, "FONT_DESCENT 2\n");
	fprintf(bdf, "ENDPROPERTIES\n");
*/

	fprintf(bdf, "STARTFONT 2.1\n");
	fprintf(bdf, "FONT -noname-%s-Medium-R-Normal--16-120-100-100-C-80-iso10646-1\n", fontname);
	fprintf(bdf, "SIZE 16 75 75\n");
	fprintf(bdf, "FONTBOUNDINGBOX 8 16 0 -4\n");
	fprintf(bdf, "STARTPROPERTIES 21\n");
	fprintf(bdf, "FOUNDRY \"noname\"\n");
	fprintf(bdf, "FAMILY_NAME \"%s\"\n", fontname);
	fprintf(bdf, "WEIGHT_NAME \"Medium\"\n");
	fprintf(bdf, "SLANT \"R\"\n");
	fprintf(bdf, "SETWIDTH_NAME \"Normal\"\n");
	fprintf(bdf, "ADD_STYLE_NAME \"\"\n");
	fprintf(bdf, "PIXEL_SIZE 16\n");
	fprintf(bdf, "POINT_SIZE 120\n");
	fprintf(bdf, "RESOLUTION_X 100\n");
	fprintf(bdf, "RESOLUTION_Y 100\n");
	fprintf(bdf, "SPACING \"C\"\n");
	fprintf(bdf, "AVERAGE_WIDTH 80\n");
	fprintf(bdf, "CHARSET_REGISTRY \"iso10646\"\n");
	fprintf(bdf, "CHARSET_ENCODING \"1\"\n");
	fprintf(bdf, "CAP_HEIGHT 10\n");
	fprintf(bdf, "X_HEIGHT 7\n");
	fprintf(bdf, "FONT_ASCENT 14\n");
	fprintf(bdf, "FONT_DESCENT 2\n");
	fprintf(bdf, "FACE_NAME \"%s unicode\"\n", fontname);
	fprintf(bdf, "COPYRIGHT \"Copyright (c) 2012 someone\"\n");
	fprintf(bdf, "DEFAULT_CHAR 0\n");
	fprintf(bdf, "ENDPROPERTIES\n");

	int nchars = sizeof(dos2unicode)/sizeof(dos2unicode[0]);

	fprintf(bdf, "CHARS %d\n", nchars);

	for (int i = 0; i < nchars; ++i)
	{
		fprintf(bdf, "STARTCHAR U+%04X\n", dos2unicode[i].uni);
		fprintf(bdf, "ENCODING %d\n", dos2unicode[i].uni);

		fprintf(bdf, "SWIDTH 500 0\n");
		fprintf(bdf, "DWIDTH 8 0\n");
		fprintf(bdf, "BBX 8 16 0 -2\n");
		fprintf(bdf, "BITMAP\n");

		char* glyph = &data[dos2unicode[i].dos * 16];

		for (int j = 0; j < 16; ++j)
		{
			fprintf(bdf, "%02X\n", (unsigned char)glyph[j]);
		}

		fprintf(bdf, "ENDCHAR\n");
	}
	fprintf(bdf, "ENDFONT\n");

	fclose(bdf);

	free(data);

	return 0;
}
















