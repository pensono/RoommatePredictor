FROM python:3.7

ENV PYTHONUNBUFFERED 1

RUN pip3 install torch==1.2.0+cu92 torchvision==0.4.0+cu92 -f https://download.pytorch.org/whl/torch_stable.html
RUN pip3 install django

RUN pip3 install allennlp --no-cache-dir
RUN python -m spacy download de_core_news_sm

RUN pip3 install emoji

COPY telegram_classifier /app/telegram_classifier
COPY trained-boe/20190805-182915/model.tar.gz /models/model.tar.gz
COPY data/processed/group_chat.json /data/group_chat.json
COPY app /app

WORKDIR /app

ENTRYPOINT ["python", "/app/manage.py", "runserver", "0.0.0.0:80"]
#ENTRYPOINT ["/bin/bash"]