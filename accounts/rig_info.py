PROCESSOR_CHOICES = (
    ('INT', 'Intel'),
    ('AMD', 'AMD'),
    ('OTH', 'Other')
)

GFX_CHOICES = (
    ('NV', 'nVidia'),
    ('AT', 'ATI'),
    ('IN', 'Intel')
)

GFX_MEMORY_CHOICES = (
    (64, '64mb'),
    (128, '128mb'),
    (1024, '1gb'),
    (2048, '2gb'),
    (4096, '4gb'),
    (0, 'Other')
)

MEMORY_TYPE_CHOICES = (
    ('SDRM', 'SDRAM'),
    ('DDR', 'DDR'),
    ('DDR2', 'DDR2'),
    ('DDR3', 'DDR3'),
    ('OTHR', 'Other')
)