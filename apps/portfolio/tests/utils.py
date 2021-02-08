from mixer.backend.django import Mixer


def create_object(model, *, data=None, commit=True):
    if data is None:
        data = {}
    mixer = Mixer(commit=commit)
    return mixer.blend(model, **data)
