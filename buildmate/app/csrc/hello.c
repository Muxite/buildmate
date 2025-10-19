#include <stdio.h>

void drawStar(int n) {
  // Draws a star with 'n' points.  Implementation is up to the user.
  // A simple implementation just prints n lines of asterisks with increasing width.

  for (int i = 1; i <= n; i++) {
    for (int j = 0; j < i; j++) {
      printf("*");
    }
    printf("\n");
  }
}

int main(){
    drawStar(5);
    return 0;
}