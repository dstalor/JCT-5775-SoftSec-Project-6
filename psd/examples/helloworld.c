#include <stdio.h>

int main()
{
	volatile int hello = 1;
	
	if(hello == 1)
	{
		printf("Hello world!\n");
	}
	else
	{
		printf("Goodbye world!;-(\n");
	}
		
	return 0;
}