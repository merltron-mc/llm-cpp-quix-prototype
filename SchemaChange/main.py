import os
from quixstreams import Application, State
from quixstreams.models.serializers.quix import QuixDeserializer, QuixTimeseriesSerializer


app = Application.Quix("transformation-v3", auto_offset_reset="earliest")

input_topic = app.topic(os.environ["input"], value_deserializer=QuixDeserializer())
output_topic = app.topic(os.environ["output"], value_serializer=QuixTimeseriesSerializer())

sdf = app.dataframe(input_topic)

sdf["chat-message"] = sdf["text"]

def update_tags(row):
    row["Tags"]["name"] = row["role"]

sdf = sdf.update(update_tags)

sdf = sdf.update(lambda row: print(row))

#sdf.to_topic(output_topic)

if __name__ == "__main__":
    app.run(sdf)