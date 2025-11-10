from hotglue_tap_sdk import typing as th

amount_schema = th.ObjectType(
    th.Property("currency", th.StringType),
    th.Property("value", th.StringType),
)
