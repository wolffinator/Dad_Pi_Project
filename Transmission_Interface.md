|State Num|Send Ready|Ack|Description|
|:--------|:--------|:--------||
|1        |False    |False    |Starting state. Raspberry pi is calculating outputs.|
|2        |True     |False    |Raspberry Pi has values in gpio pins and awaits Ack from circuit|
|3        |True     |True     |Raspberry Pi collects next frame of information from accelerometer and will dissable Send Ready after collection|
|4        |False    |True     |Raspberry Pi is calculating outputs and awaits Ack to be False.|