import numpy as np
from hmmlearn import hmm
import mido

N=20 #Nombre d'états cachés
iteration=20 #Nombre d'itération
instrument=0 #Numéro de l'instrument à jouer
dureeNote=300 #Durée d'une note

##Modèle continue
#Définition du modèle
model = hmm.GaussianHMM(n_components=N, covariance_type="full",init_params="mc")

A=np.ones((N,N))/N
PI=np.ones((N))/N

model.startprob_=PI
model.transmat_=A
model.n_iter=iteration


#Apprentissage
mid = mido.MidiFile("C:\\Users\\benoi\\OneDrive\\Bureau\\Cours_ei2\\Projet musique aléatoire\\Basededonnée\\Musique (7).mid", clip=True)
track=mid.tracks[0]
y=[]
for msg in track:
    if msg.type=='note_on':
        if msg.velocity !=0:
            y.append([msg.note])

model.fit(y)


#Création de la chanson
X,Z=model.sample(100)

mid1=mido.MidiFile()
track=mido.MidiTrack()
track.append(mido.Message('program_change',program=instrument, time=0))
for i in X :
    track.append(mido.Message('note_on',note=(int(i)),velocity=80,time=10))
    track.append(mido.Message('note_off',note=(int(i)),velocity=80,time=int(dureeNote*(1+i%1)[0])))
mid1.tracks.append(track)
mid1.save('test.mid')
