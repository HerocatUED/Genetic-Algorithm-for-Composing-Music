# Genetic-Algorithm-for-Composing-Music
Final Project of Music and Math (PKU 2023 Autumn)

# Quick Start
1. install requirements with following command ```pip install -r requirements.txt```
2. put your midi files under folder **data**, these will be the initial population.
3. run pipeline ```python pipeline.py```
4. check results in folder **result/midis**
5. choose one midi file, run following command to get chords that matches the melody. 
   ```python pipeline.py --mode test --id $your-midi-id$``` 

# Demo
You can find a .mp3 file in folder **doc**. We generated it with our codes, and manually add chords given by our program.
