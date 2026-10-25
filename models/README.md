# GreenLoop waste model

`waste_mobilenetv2.onnx` and `waste_mobilenetv2_labels.txt` are from the
[iAny waste-material classifier](https://huggingface.co/sengtha/iany-waste-v1),
released under **Creative Commons Attribution 4.0 International (CC BY 4.0)**.

Attribution: **iAny (E-KHMER Technology), iany-waste-v1**. The model card says
it was trained on open waste datasets including TrashNet and two waste image
datasets, and notes that it is a beta suggestion model. Keep this attribution
if the model is redistributed.

The seven model outputs are `can`, `glass`, `organic`, `other`, `paper`,
`plastic_bottle`, and `plastic_other`. GreenLoop maps cans to Metal and both
plastic labels to Plastic. The model runs locally with ONNX Runtime; it does not
send uploaded photos anywhere. It works best with one clear, centered item in a
well-lit photo. It can still be wrong and does not replace local recycling rules.
