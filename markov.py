import ast

fin = open("alt.txt", "r")
data = fin.read().split("\n")[:-1]
fin.close()

# Parse transcripts
transcripts = []
skip = 0
import random

for s in range(0, len(data)):
    script = ast.literal_eval(data[s])["transcript"].split("\n")
    parsed = []
    for i in range(0, len(script)):
        if skip > 0:
            skip-=1
            continue
            
        if script[i] == "":
            continue
        if i == len(script)-1:
            authdiv = script[i].find(": ")
            if authdiv < 0:
#                print("No authdiv on %d" % s)
                continue
            parsed.append( ("Alt-Text", script[i][authdiv+2:-2]) )
        elif (script[i][:2] == "[[" and script[i][-2:] == "]]") or (script[i][:2] == "((" and script[i][-2:] == "))"):
            parsed.append( ("Description", script[i][2:-2]) )
        elif script[i][:2] == "{{" and script[i][-2:] == "}}":
            parsed.append( ("Narrator", script[i][2:-2]) )
        elif script[i][:2] == "[[" and script[i][-2:] != "]]":
            authend = script[i].find("]]")
            if authend < 0:
#                print("No authend on %d" % s)
                continue
            parsed.append( (script[i][2:authend], script[i][authend+1:]) )
        else:
            authdiv = script[i].find(": ")
            if authdiv < 0 or authdiv > 70:
                if script[i].lower() == script[i] and len(parsed) > 0:
                    parsed[-1] = (parsed[-1][0], parsed[-1][1]+script[i])
                    continue
                parsed.append( ("", script[i]) )
                continue
            elif authdiv == len(script[i].strip())-1:
                parsed.append( (script[i].strip()[:-1], script[i+1]) )
                skip = 1
                continue
            parsed.append( (script[i][:authdiv], script[i][authdiv+2:]) )
    transcripts.append(parsed)

# Build list of Speakers with weights
speakers = {}
speakers_n = 0
for s in transcripts:
    for l in s:
        if l[0] == "Description" or l[0] == "Alt-Text" or l[0] == "Narrator" or l[0] == "":
            continue
        if l[0] in speakers:
            speakers[l[0]] += 1
        else:
            speakers[l[0]] = 1
        speakers_n+=1

speakers_k = list(speakers.keys())
def get_speaker():
    global speakers_k
    
    r = random.randrange(0, speakers_n)
    for k in speakers_k:
        r -= speakers[k]
        if r < 0:
            return k

# Build markov structure\
# {previous word: [# of times previous word appeared in text, {New word that followed previous word: # of times new word followed previous word, ...}]}
description_m = {}
narrator_m = {}
alt_text_m = {}
speaker_m = {}

for s in transcripts:
    for l in s:
        if l[0] == "Description":
            targ = description_m
        elif l[0] == "Narrator":
            targ = narrator_m
        elif l[0] == "Alt-Text":
            targ = alt_text_m
        else:
            targ = speaker_m
        
        prev = ""
        word = ""
        for c in l[1]:
            c = c.lower()
            if c in "abcdefghijklmnopqrstuvwxyz0123456789%$#@^*|<>-_=+':;/\\`~":
                word = word + c
            elif c in " \t\n,.!?&":
                if prev in targ:
                    targ[prev][0]+=1
                    if word in targ[prev][1]:
                        targ[prev][1][word]+=1
                    else:
                        targ[prev][1][word] = 1
                else:
                    targ[prev] = [1, {word: 1}]
                
                prev = word
                if c in ",.!?&":
                    word = c
                else:
                    word = ""

characters_n = random.randrange(2, 6)
characters = []
for i in range(0, characters_n):
    characters.append(get_speaker())

characters = characters + ["Description", "Narrator"]

transcript_lines_n = random.randrange(5, 12) + random.randrange(5, 12)

markov_script = []
for i in range(0, transcript_lines_n):
    if i == transcript_lines_n - 1:
        speaker = "Alt Text"
        targ = alt_text_m
    else:
        speaker = characters[random.randrange(0, len(characters))]
        if speaker == "Description":
            targ = description_m
        elif speaker == "Narrator":
            targ = narrator_m
        else:
            targ = speaker_m
    
    line = ""
    for w in range(0, 50):
        word = ""
        word_n = targ[word][0]
        
        r = random.randrange(0, word_n)
        word_k = list(targ[word][1].keys())
        for k in word_k:
            r -= targ[word][1][k]
            if r < 0:
                word = k
                break
        if line == "" or word in ",.!?" or word == "":
            line = line + word
        else:
            line = line + " " + word
        
        if word == "." or word == "!" or word == "?":
            break
    
    markov_script.append((speaker, line[0].upper() + line[1:]))

final_transcript = ""
for l in markov_script:
    if l[0] == "Narrator":
        final_transcript = final_transcript + "{{" + l[1] + "}}\n"
    elif l[0] == "Description":
        final_transcript = final_transcript + "[[" + l[1] + "]]\n"
    else:
        final_transcript = final_transcript + l[0] + ": " + l[1] + "\n"

print(final_transcript)