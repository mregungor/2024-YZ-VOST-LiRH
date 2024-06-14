from RealtimeSTT import AudioToTextRecorder
import os

if __name__ == '__main__':

    print("Initializing RealtimeSTT test...")

    full_sentences = []
    displayed_text = ""

    def clear_console():
        os.system('clear' if os.name == 'posix' else 'cls')

    def text_detected(text):
        global displayed_text
        sentences = " ".join(full_sentences)
        new_text = sentences + " " + text if sentences else text

        if new_text != displayed_text:
            displayed_text = new_text
            clear_console()
            print(displayed_text, end="", flush=True)

    def process_text(text):
        full_sentences.append(text)
        text_detected("")

    recorder_config = {
        'spinner': False,
        'model': 'small',
        'language': 'tr',
        'silero_sensitivity': 0.2, #Daha düşük değerler daha fazla algılamaya ve hatalı tanımaya neden olabilirken, daha yüksek değerler daha az algılamaya neden olabilir.
        'webrtc_sensitivity': 1, #Bu, gerçek zamanlı işleme duyarlılığını kontrol eder.
        'post_speech_silence_duration': 0.2, #Konuşma algılandıktan sonraki sessizlik süresini belirtir. Bu, konuşma tanıma sonrası sessizlik süresini ayarlar.
        'min_length_of_recording': 0,
        'min_gap_between_recordings': 0,
        'enable_realtime_transcription': True,
        'realtime_processing_pause': 0.1, #Gerçek zamanlı işleme arasındaki duraklama süresini belirtir. Saniye cinsinden bir süre olarak ayarlanır.
        'realtime_model_type': 'base', #Gerçek zamanlı transkript için kullanılacak model tipini belirtir.
        'on_realtime_transcription_update': text_detected,
    }

    recorder = AudioToTextRecorder(**recorder_config)

    print("Say something...", end="", flush=True)

    while True:
        recorder.text(process_text)
