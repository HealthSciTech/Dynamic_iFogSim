#include <stdio.h>
int cycle_total, instr_total, frequency;
float avg_cpi;

void menu(){
   printf("\nMenu of Options: \n----------------\n");
   printf("1) Enter parameters\n");
   printf("2) Calculate average CPI of a sequence of instructions\n");
   printf("3) Calculate total execution time of a sequence of instructions\n");
   printf("4) Calculate MIPS of a sequence\n");
   printf("5) Quit\n");
   printf("\nEnter selection: ");
}

void enter_params(){ //selection 1
   int i, cpi_class, instr_count, num_classes; //declaring local variables

   printf("\nEnter number of instruction classes: ");//user prompts
   scanf("%d", &num_classes);
   printf("Enter the frequency of the machine (MHz): ");
   scanf("%d", &frequency);

   for(i = 1; i <= num_classes; i++){
      printf("Enter the CPI of class %d: ", i);//more prompts
      scanf("%d", &cpi_class);
      printf("Enter instruction count of class %d (millions): ", i);
      scanf("%d", &instr_count);
      cycle_total += (cpi_class * instr_count);//calculation
      instr_total += instr_count;
   }
}

void calc_cpi(){ //selection 2
   avg_cpi = (float) cycle_total / (float) instr_total;
   printf("The average CPI of the sequence is: %.2f\n", avg_cpi);
}

void calc_exec(){ //selection 3
   float exec_time;
   exec_time = (cycle_total/(1.0 * frequency))*1000;
   printf("The total CPU time of the sequence is: %.2f msec\n", exec_time);
}

void calc_mips(){ //selection 4
   float mips;
   mips = frequency/avg_cpi;
   printf("The total MIPS of the sequence is: %.2f\n", mips);
}

int main(){
   int choice = 0;
   while(choice != 5){
      menu();
      scanf("%d", &choice);

      switch(choice){
         case 1: enter_params(); break;
         case 2: calc_cpi(); break;
         case 3: calc_exec(); break;
         case 4: calc_mips(); break;
         case 5: choice = 5; break;
         default: printf("Switch statement hit default case"); break;
      }
   }
   return -1;
}
