byte buffer[50];

void setup()
{
    Serial.begin(115200);
}

bool read_meta = false;
bool read_seq = false;

uint16_t sequence[100][3];
unsigned seq_length = 0; 
unsigned tempo = 0;
unsigned total_seq_length = 0;

void loop()
{
    if (not read_meta && not read_seq && Serial.available() > 1 )
    {
        Serial.readBytes(buffer, 2);
        tempo = buffer[0];
        total_seq_length = buffer[1];
        read_meta = true;
    }

    if (read_meta && not read_seq && Serial.available() > 3)
    {   
        Serial.readBytes(buffer, 4);

        unsigned note = (unsigned) buffer[0];
        unsigned velocity = (unsigned) buffer[1];
        uint16_t msg_time = ((unsigned) buffer[2] << 8) | (unsigned) buffer[3]; 
        sequence[seq_length][0] = note;
        sequence[seq_length][1] = velocity;
        sequence[seq_length][2] = msg_time;
        seq_length++;
        if (seq_length == total_seq_length) read_seq = true;    
    }

    if (read_seq)
    {
        for (int i = 0; i < seq_length; ++i)
        {
            uint16_t msg[3] = sequence[i];

            delay(msg[2]);
            pick_note(msg[0]);
            if (msg[1] > 0)
            {
                
            } 

        }
    }
}