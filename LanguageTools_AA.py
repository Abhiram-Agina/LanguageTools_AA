import easyocr #Converts Image to Text - Optical Character Recognition
import streamlit as st #Create Apps of Python Programs + Hosting
from PIL import Image #Image Manipulation
import numpy as np #Numeric Procesing
import speech_recognition as sr #Speech to Text
from mtranslate import translate #Language Translation
from gtts import gTTS #Text to Speech

import re #pip install regex #for handling regular expressions #String Manipulation
import random 
import sys

reader = easyocr.Reader(['en', 'es', 'de', 'fr']) # need to run only once to load model into memory

r = sr.Recognizer()

st.title("Language Learning Tools")

st.sidebar.image('images/AbhiramAgina.png', use_column_width=True)
st.sidebar.markdown('I am a Junior at Oak Park High School in Oak Park, CA. My friends and I learn Foreign Languages, so I built this App to make things easier. My goal is to bring all Language Learning Tools under one roof. Please check it out.')

nav = st.sidebar.radio("Navigation",["Image-to-Text","Text-Translate","Text-to-Speech", "Speech-to-Text", "Chat-with-Eliza"])
st.image('images\WorldLanguages.jpg', width=400)

# Language ISO Codes used by Python: https://cloud.google.com/translate/docs/languages
src = st.sidebar.selectbox('from', ['en', 'es', 'de', 'fr', 'zh-CN', 'zh-TW'])
tgt = st.sidebar.selectbox('to', ['en', 'es', 'de', 'fr', 'zh-CN', 'zh-TW'])


if nav == "Image-to-Text":
    st.header("OCR: extract text from image")
    image = st.file_uploader(label = "upload your image here", type=['png','jpg','jpeg'])

    if image is not None:
        input_image = Image.open(image)
        st.image(input_image)

    if st.button("Extract"):
        if image is not None:
            with st.spinner("AI is at work!"):              
                result = reader.readtext(np.array(input_image))
                result_text = []
                for text in result:
                    result_text.append(text[1])
            st.success("here you go!")
            Imagetext = ' '.join(result_text)
            st.write(Imagetext)
            output = translate(Imagetext,tgt)
            st.text_area("Translated Text is ",output,height=200)
            
            
if nav == "Text-Translate":
    st.header("Translator: multiple languages")  
    text_src = st.text_area("Enter text:", height=200)
    
    if st.button('Translate Sentence'):
        if text_src == "":
            st.warning('Please **enter text** for translation')

        else:
            text_tgt = translate(text_src,tgt)
            st.write(text_tgt) 
            
           
           
if nav == "Text-to-Speech":
    st.header("Text-to-Speech Conversion")  
    st.write('Listen to source text in the source language')
    
    text_src = st.text_area("Enter text:", height=200)
    
    if st.button('Text-to-Speech'):
        if text_src == "":
                st.warning('Please **enter text** for translation')
        else:
            text_tgt = translate(text_src,tgt) 
                
            es_tts=gTTS(text_src, lang=src) #target language here is Spanish accent of the OCR Text       
            es_tts.save('trans.mp3') #convert the original text into an audio file

            audio_file = open('trans.mp3', 'rb')
            audio_bytes = audio_file.read()
            st.audio(audio_bytes,format='audio/mp3')
            
            
if nav == "Speech-to-Text":
    st.title("Convert Audio to Text")
    uploadedAudioFile = st.file_uploader(label = "Upload your audio file here", type=['wav'])
    st.write("Note: This accepts .wav files only. Convert from MP3 to WAV using https://cloudconvert.com/mp3-to-wav")

    if uploadedAudioFile is not None:
        st.header("Uploaded Audio: Original")
        audio_bytes = uploadedAudioFile.read()
        st.audio(audio_bytes,format='audio/wav') #this will let user play the user-uploaded audio file
        
        sound = uploadedAudioFile.name
        with sr.AudioFile(sound) as source:
            audio_data = r.record(source)
            text_src = r.recognize_google(audio_data, language=src) # 'es-ES'
            st.header("Transcribed Text")
            st.write(text_src)
        
        st.header("Translated Text")
        text_tgt = translate(text_src,tgt)
        st.write(text_tgt)
        
        st.header("Text-to-Speech Conversion: Translated")  
        st.write('Listen to source text in the target language')
        es_tts=gTTS(text_tgt, lang=tgt) #target language here is Spanish accent of the OCR Text       
        es_tts.save('transT.mp3') #convert the original text into an audio file
        audio_file = open('transT.mp3', 'rb')
        audio_bytes = audio_file.read()
        st.audio(audio_bytes,format='audio/mp3')
        
        
if nav == "Chat-with-Eliza":
    st.write("DISCLAIMER: Please note that the automated text/translation may result in unexpected outcomes. If EIZA misbehaves, let me know.")
    # reflejos sobre el sujeto
    reflections = {
        "estoy": "estas",
        "soy": "eres",
        "fui": "fuiste",
        "yo": "tu",
        "deberia": "deberias",
        "tengo": "tienes",
        "quiero": "quieres",
        "mio": "tuyo",
        "eres": "soy",
        "tu tienes": "yo tengo",
        "tu seras": "yo sere",
        "tuyo": "mio",
        "vuestro": "nuestro",
        "sobre ti": "sobre mi",
        "sobre mi": "sobre ti"
    }

    # patrones psicologicos más probables
    psychobabble = [
        [r'Yo (necesito|quiero|deseo) (.*)',
         ["¿Por qué necesitas {0}?",
          "¿Realmente te ayudaría a obtener {0}?",
          "¿Estás seguro de que necesitas {0}?"]],

        [r'por que no puedes ([^\?]*)\??' or r'por qué no puedes ([^\?]*)\??',
         ["¿De verdad crees que no lo hago? {0}?",
          "Tal vez eventualmente lo haré. {0}.",
          "¿De verdad quieres que yo {0}?"]],

        [r'¿Por que no puedo ([^\?]*)\??' or r'por que no puedo ([^\?]*)\??' or r'¿Por qué no puedo ([^\?]*)\??' or r'Por qué no puedo ([^\?]*)\??',
         ["¿Crees que deberías ser capaz de {0}?",
          "Si pudieras {0}, ¿qué harías?",
          "No sé - ¿por qué no puedes {0}?",
          "¿Lo has intentado realmente?"]],

        [r'no puedo(.*)',
         ["¿Cómo sabes que no puedes{0}?",
          "Tal vez podría {0} si lo intentó.",
          "¿Qué se necesita para que usted {0}?"]],

        [r'yo soy (.*)',
         ["¿Has venido a mí porque eres  {0}?",
          "¿Cuánto tiempo has estado {0}?",
          "¿Cómo te sientes acerca de ser {0}?"]],

        [r'estoy (.*)',
         ["¿Cómo te hace sentir{0}?",
          "¿Te gusta ser {0}?",
          "¿Por qué me dices que eres{0}?",
          "¿Por qué crees que eres  {0}?"]],

        [r'¿ ([^\?]*)\??',
         ["¿Por qué importa si soy {0}?",
          "¿Lo preferirías si no fuera {0}?",
          "Tal vez usted piensa que soy.",
          "Puedo ser {0} - ¿qué piensas?"]],

        [r'¿qué (.*)' or r'qué (.*)' or r'que (.*)',
         ["¿Por qué preguntas?",
          "¿Cómo le ayudaría una respuesta a eso?",
          "¿Qué piensas?"]],

        [r'¿cómo (.*)' or r'cómo (.*)' or r'como (.*)',
         ["¿Cómo se supone?",
          "Tal vez puedas responder a tu propia pregunta.",
          "¿Qué estás realmente pidiendo?"]],

        [r'porque (.*)',
         ["¿Es esa la verdadera razón?",
          "¿Qué otras razones vienen a la mente?",
          "¿Esa razón se aplica a cualquier otra cosa?",
          "Si {0}, ¿qué otra cosa debe ser verdadera?"]],

        [r'(.*) lo siento (.*)',
         ["Hay muchas veces cuando no se necesita disculpa.",
          "¿Qué sentimientos tiene cuando se disculpa?"]],

        [r'hola(.*)',
         ["Hola ... me alegro de que puedas pasar por hoy.",
          "¿Hola, cómo estas hoy?",
          "Hola, ¿cómo te sientes hoy?"]],

        [r'pienso (.*)',
         ["¿Dudas {0}?",
          "¿De verdad piensas eso?",
          "Pero no estás seguro {0}?"]],

        [r'(.*) amigo (.*)',
         ["Cuéntame más sobre tus amigos.",
          "Cuando piensas en un amigo, ¿qué te viene a la mente?",
          "¿Por qué no me hablas de un amigo desde la infancia?"]],

        [r'si',
         ["Pareces muy seguro.",
          "Está bien, pero ¿puedes hacer algo?"]],

        [r'(.*) ordenador(.*)',
         ["¿De verdad estás hablando de mí?",
          "¿Parece extraño hablar con una computadora?",
          "¿Cómo te hacen sentir las computadoras?",
          "¿Se siente amenazado por las computadoras?"]],

        [r'eso es (.*)',
         ["¿Crees que es {0}?",
          "Tal vez sea {0} - ¿qué piensas?",
          "Si fuera {0}, ¿qué harías?",
          "Podría ser que {0}."]],

        [r'es eso (.*)',
         ["Pareces muy seguro.",
          "Si te dijera que probablemente no es {0}, ¿qué sentirías?"]],

        [r'¿puedes ([^\?]*)\??',
         ["¿Qué te hace pensar que no puedo {0}?",
          "Si pudiera {0}, ¿entonces qué?",
          "¿Por qué me preguntas si puedo (0)?"]],

        [r'puedo ([^\?]*)\??',
         ["No puedes querer {0}.",
          "¿Quieres ser capaz de {0}?",
          "Si pudieras {0}, ¿cierto?"]],

        [r'tu eres (.*)' or r'¿tu eres (.*)',
         ["¿Por qué crees que soy {0}?",
          "¿Te gusta pensar que soy {0}?",
          "Tal vez usted quiere que sea.",
          "¿Tal vez estás hablando de ti?"]],

        [r'¿eres ture (.*)',
         ["¿Por qué dices que soy {0}?",
          "¿Por qué crees que soy {0}?",
          "¿Estamos hablando de ti o de mí?"]],

        [r'¿no lo hago (.*)',
         ["No realmente {0}?",
          "¿Por qué no {0}?",
          "¿Quieres {0}?"]],

        [r'me siento (.*)',
         ["Bueno, cuéntame más sobre estos sentimientos.",
          "¿Sientes a menudo {0}?",
          "¿Cuándo sientes normalmente {0}?",
          "Cuando sientes {0}, ¿qué haces?"]],

        [r'yo tengo (.*)',
         ["¿Por qué me dices que tienes {0}?",
          "¿Realmente tienes {0}?",
          "Ahora que tienes {0}, ¿qué harás después?"]],

        [r'yo debo (.*)',
         ["¿Podría explicar por qué lo haría?",
          "¿Por que lo harias?",
          "¿Quién más sabe que lo harías?"]],

        [r'esta ahí (.*)',
         ["¿Crees que hay {0}?",
          "Es probable que haya {0}.",
          "¿Te gustaría tener {0}?"]],

        [r'mi (.*)',
         ["Ya veo, tu {0}.",
          "¿Por qué dices que tu {0}?",
          "Cuando tu {0}, ¿cómo te sientes?"]],

        [r'tu (.*)',
         ["debemos estar discutiendo contigo, no conmigo.",
          "¿Por qué dices eso de mí?",
          "¿Por qué te importa si yo {0}?"]],

        [r'por qué (.*)',
         ["¿Por qué no me dices la razón por la cual {0}?",
          "¿Por qué crees que {0}?"]],

        [r'quiero que (.*)',
         ["¿Qué significaría para ti si tienes {0}?",
          "¿Por qué quieres {0}?",
          "¿Qué harías si tuvieras {0}?",
          "Si tienes {0}, entonces ¿qué harías?"]],

        [r'(.*) madre(.*)',
         ["Cuéntame más sobre tu madre.",
          "¿Cómo era tu relación con tu madre?",
          "¿Cómo te sientes con tu madre?",
          "¿Cómo se relaciona esto con tus sentimientos hoy?",
          "Las buenas relaciones familiares son importantes."]],

        [r'(.*) padre(.*)',
         ["Cuéntame más sobre tu padre.",
          "¿Cómo te hizo sentir tu padre?",
          "¿Cómo te sientes con tu padre?",
          "¿Su relación con su padre se relaciona con sus sentimientos hoy?",
          "¿Tiene problemas para mostrar afecto con su familia?"]],

        [r'(.*) niño(.*)',
         ["¿Tenías amigos íntimos cuando era niño?",
          "¿Cuál es tu recuerdo favorito de la niñez?",
          "¿Recuerdas algún sueño o pesadilla desde la infancia?",
          "¿Alguna vez te han molestado los otros niños?",
          "¿Cómo crees que tus experiencias infantiles se relacionan con tus sentimientos hoy?"]],

        [r'(.*)\?',
         ["¿Porque preguntas eso?",
          "Por favor, considere si puede responder a su propia pregunta.",
          "¿Quizás la respuesta está dentro de ti?",
          "¿Por qué no me lo dices?"]],

        [r'adios',
         ["Gracias por hablar conmigo.",
          "Adiós.",
          "Gracias, eso será $ 150. ¡Que tengas un buen día!"]],

        [r'(.*)',
         ["Por favor, cuéntame más.",
          "Vamos a cambiar de enfoque un poco ... Háblame de tu familia.",
          "¿Puedes profundizar sobre eso?",
          "¿Por qué dices eso {0}?",
          "Ya veo.",
          "Muy interesante.",
          "{0}.",
          "Ya veo, ¿y qué te dice eso?",
          "¿Cómo te hace sentir eso?",
          "¿Cómo te sientes cuando dices eso?"]]
    ]


    def reflect(fragment):
        tokens = fragment.lower().split()
        for i, token in enumerate(tokens):
            if token in reflections:
                tokens[i] = reflections[token]
        return ' '.join(tokens)
        
    def analyze(statement):
        for pattern, responses in psychobabble:
            match = re.match(pattern, statement.rstrip(".!"))
            if match:
                response = random.choice(responses)
                return response.format(*[reflect(g) for g in match.groups()])

    st.image('images\Eliza.gif')
    st.write("To learn more about me: https://www.youtube.com/watch?v=RMK9AphfLco") 
    #st.write("Hola ¿Cómo te sientes hoy?")

    #create cache object for the "chat"
    @st.cache(allow_output_mutation=True)
    def Chat():
        return []    

    statement = st.text_input("Post your message here:")

    try:
        #messages = zip(*chat)
        #st.table(statement)
        #st.write(analyze(statement))
        if statement == "quit":
            sys.exit()       
    except ValueError:
        st.title("Enter your message into the chat window, and post!")

    chat=Chat()

    if st.button("Post"): #Needs Enhancement: allow chat by pressing enter, instead of clicking on button.
        if statement == "":
            st.warning('Please **enter message** to chat with Eliza')
        chat.append(statement)
        st.write(analyze(statement))

    if len(chat) > 10:
        del(chat[0])
           
else:
  pass
