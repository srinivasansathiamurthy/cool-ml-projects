from datasets import load_dataset
import torch
from torchaudio.transforms import MelSpectrogram
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
from torch.utils.data import DataLoader
import numpy as np
from scipy.fft import fft
from scipy.signal import savgol_filter
from torchmetrics.functional import soft_dtw

class BaseModel:
    def __init__(self):
        self.dataset = load_dataset("ShoukanLabs/AniSpeech")
        self.processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-base-960h")
        self.model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-base-960h")
        self.mel_spectrogram = MelSpectrogram()
        self.train_loader = None
        self.num_epochs = 50

    def prepare_data(self):
        def preprocess(batch):
            audio = batch["audio"]
            batch["input_values"] = self.processor(audio["array"], sampling_rate=audio["sampling_rate"]).input_values[0]
            batch["labels"] = self.processor(batch["caption"]).input_ids
            return batch

        self.dataset = self.dataset.map(preprocess, remove_columns=self.dataset["train"].column_names)
        self.train_loader = DataLoader(self.dataset["train"], batch_size=8, shuffle=True)

    def train(self):
        self.model.train()
        optimizer = torch.optim.AdamW(self.model.parameters(), lr=1e-4)
        for epoch in range(self.num_epochs):
            for batch in self.train_loader:
                input_values = torch.tensor(batch["input_values"]).to(self.model.device)
                labels = torch.tensor(batch["labels"]).to(self.model.device)
                optimizer.zero_grad()
                outputs = self.model(input_values, labels=labels)
                loss = outputs.loss
                loss.backward()
                optimizer.step()
                print(f"Epoch {epoch}, Loss: {loss.item()}")

class LossMetricsBuilder:
    def __init__(self):
        pass

    def transform_audio(self, audio):
        signal = fft(audio)
        return signal

    def smooth_signal(self, signal):
        smoothed_signal = savgol_filter(signal, window_length=5, polyorder=2)
        return smoothed_signal

    def compute_loss(self, audio1, audio2):
        signal1 = self.transform_audio(audio1)
        signal2 = self.transform_audio(audio2)
        smoothed_signal1 = self.smooth_signal(signal1)
        smoothed_signal2 = self.smooth_signal(signal2)
        loss = soft_dtw(torch.tensor(smoothed_signal1), torch.tensor(smoothed_signal2))
        return loss
