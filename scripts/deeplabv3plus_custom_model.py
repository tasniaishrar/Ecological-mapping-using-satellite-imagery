_base_ = [
    '../_base_/models/deeplabv3plus_custom.py',
    '../_base_/datasets/openearthmap.py', '../_base_/default_runtime.py',
    '../_base_/schedules/schedule_80k.py'
]
model = dict(
    decode_head=dict(num_classes=9), auxiliary_head=dict(num_classes=9))