this repo uses librosa to edit out the parts of a wav audiofile that contain white noise


app2 genera il power spectrogram dal mean_power
per i gqrx recordings (49 db LNA, -8db gain) la potenza del white noise-static supera 
i 475 units
per i sounds(automatic recordings), il white noise ha potenza molto bassa (per via del basso guadagno di rtl_fm)

app3 trimma il white noise
per i gqrx recordings (49 db LNA, -8db gain) metti threshold < 475
per i sounds(automatic recordings) metti threshold < 18
current settings per rtl_fm
command = f"rtl_fm -f 145575000 -s 12500 -g 49 -p 1 -M fm | sox -t raw -r 12500 -e signed -b 16 -c 1 - -t wav -r 12500 -e signed -b 16 -c 1 {filename}"
white noise ha potenza >18 di notte e >23 di giorno. mantieni il setting notturno così non devi modificare lo script ogni volta;

app4 trimma il white noise
per i sounds(automatic recordings) metti threshold > 2.5

app5 è per i vecchi audio, come test, e prende tutti i files inside a folder

app6 trimma con un buffer di 15 time units(circa 250ms) così le parole non vengono tranciate quando si parla piano

app7 fa quel che fa app6 con tutti i files inside a folder

app2_new.py is like app2.py but with reduced memory usage when computing the fft on long audios (dividing correctly the audio in 10s chunks)
