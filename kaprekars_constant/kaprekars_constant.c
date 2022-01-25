#include <stdio.h>
#include <stdlib.h>

int *int_to_4_arr(int number)
{
    int *returnarr = (int*)malloc(sizeof(int) * 4);
    if (number >= 10000 || returnarr == NULL)
    {
        return NULL;
    }
    for (int i = 3; i >= 0; i--)
    {
        returnarr[i] = number % 10;
        number = number / 10;
    }
    return returnarr;
}

int *reverse_int_arr(int arr[], int n)
{
    int *new_arr = (int*)malloc(sizeof(int) * n);
    if (new_arr != NULL)
    {
        for (int i = n-1; i >= 0; i--)
        {
            new_arr[i] = arr[n-i-1];
        }
    }
    return new_arr;
}

int arr_to_number(int arr[], int n)
{
    int number = 0;
    int arr_pos = 0;
    while (arr_pos < n-1)
    {
        number = number + arr[arr_pos];
        number = number * 10;
        arr_pos++;
    }
    number = number + arr[arr_pos];
    return number;
}

static int int_compare(const void *p1, const void *p2)
{
    int int_a = * ( (int*) p1 );
    int int_b = * ( (int*) p2 );

    if ( int_a == int_b ) return 0;
    else if ( int_a < int_b ) return -1;
    else return 1;
}

int kaprekars_constant_step(int number)
{
    int *number_arr = int_to_4_arr(number);
    if (number_arr != NULL)
    {
        qsort(number_arr, 4, sizeof(int), int_compare);
        int *dsc_number_arr = reverse_int_arr(number_arr, 4);
        if (dsc_number_arr != NULL)
        {
            int first = arr_to_number(dsc_number_arr, 4);
            int second = arr_to_number(number_arr, 4);
            return first - second;
        }
    }
    return -1;
}

int kaprekars_constant_rounds(int number)
{
    int round = 0;
    do
    {
        number = kaprekars_constant_step(number);
        round++;
        if (round > 10)
        {
            round = -1;
            break;
        }
    } while (number != 6174 && number != -1);
    return round;
}

int main(void)
{
    for (int i = 1; i < 10000; i++)
    {
        printf("%d - %d\n", i, kaprekars_constant_rounds(i));
    }
    return 0;
}