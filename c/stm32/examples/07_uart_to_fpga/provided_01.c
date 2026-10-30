void polling_routine(void)
{
    int ch = getchar();
    if (ch != EOF)
    {
        uint8_t data = (uint8_t)ch;
        HAL_StatusTypeDef result =
            HAL_UART_Transmit(&huart3, &data, 1U, 100U);
        printf("전송 결과: %d\r\n", (int)result);
    }
}
