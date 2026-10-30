void polling_routine(void)
{
    int ch = getchar();
    if (ch != EOF)
    {
        printf("받은 문자: %c\r\n", ch);
    }
}
