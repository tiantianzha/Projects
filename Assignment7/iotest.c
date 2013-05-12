#include <stdio.h>

int main(void) {
   int c;
   int i = 0;
   while ((c = getchar()) != EOF) {
      printf("chararacter %d is %c", i, c);
      i++;
   }
   return 0;
}
