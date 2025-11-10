"""Stream type classes for tap-ebay."""

from hotglue_tap_sdk import typing as th

from tap_ebay.client import EbayStream
from tap_ebay.schema_helper import amount_schema
import datetime

class OrdersStream(EbayStream):
    """Define custom stream."""

    name = "orders"
    path = "/sell/fulfillment/v1/order"
    primary_keys = ["orderId"]
    replication_key = "lastModifiedDate"
    records_jsonpath = "$.orders[*]"

    @property
    def minimum_start_time(self) -> datetime.datetime:
        # orders endpoint only supports a maximum of 729 days, docs say 2 years but it fails with 2 years, works with 729 days
        return datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=729)

    schema = th.PropertiesList(
        th.Property("orderId", th.StringType),
        th.Property("legacyOrderId", th.StringType),
        th.Property("creationDate", th.DateTimeType),
        th.Property("lastModifiedDate", th.DateTimeType),
        th.Property("orderPaymentStatus", th.StringType),
        th.Property("orderFulfillmentStatus", th.StringType),
        th.Property("salesRecordReference", th.StringType),
        th.Property("sellerId", th.StringType),
        th.Property(
            "buyer",
            th.ObjectType(
                th.Property("username", th.StringType),
                th.Property(
                    "buyerRegistrationAddress",
                    th.ObjectType(
                        th.Property("fullName", th.StringType),
                        th.Property(
                            "contactAddress",
                            th.ObjectType(
                                th.Property("addressLine1", th.StringType),
                                th.Property("addressLine2", th.StringType),
                                th.Property("city", th.StringType),
                                th.Property("countryCode", th.StringType),
                                th.Property("county", th.StringType),
                                th.Property("postalCode", th.StringType),
                                th.Property("stateOrProvince", th.StringType),
                            ),
                        ),
                        th.Property("email", th.StringType),
                        th.Property("fullName", th.StringType),
                        th.Property(
                            "primaryPhone",
                            th.ObjectType(th.Property("phoneNumber", th.StringType)),
                        ),
                    ),
                ),
                th.Property(
                    "taxAddress",
                    th.ObjectType(
                        th.Property("city", th.StringType),
                        th.Property("countryCode", th.StringType),
                        th.Property("postalCode", th.StringType),
                        th.Property("stateOrProvince", th.StringType),
                    ),
                ),
                th.Property(
                    "taxIdentifier",
                    th.ObjectType(
                        th.Property("taxpayerId", th.StringType),
                        th.Property("taxIdentifierType", th.StringType),
                        th.Property("issuingCountry", th.StringType),
                    ),
                ),
            ),
        ),
        th.Property(
            "cancelStatus",
            th.ObjectType(
                th.Property("cancelledDate", th.DateTimeType),
                th.Property("cancelState", th.StringType),
                th.Property(
                    "cancelRequests",
                    th.ArrayType(
                        th.ObjectType(
                            th.Property("cancelCompletedDate", th.DateTimeType),
                            th.Property("cancelInitiator", th.StringType),
                            th.Property("cancelReason", th.StringType),
                            th.Property("cancelRequestedDate", th.DateTimeType),
                            th.Property("cancelRequestId", th.StringType),
                            th.Property("cancelRequestState", th.StringType),
                        )
                    ),
                ),
            ),
        ),
        th.Property(
            "lineItems",
            th.ArrayType(
                th.ObjectType(
                    th.Property("lineItemId", th.StringType),
                    th.Property("title", th.StringType),
                    th.Property("sku", th.StringType),
                    th.Property("quantity", th.IntegerType),
                    th.Property("legacyItemId", th.StringType),
                    th.Property("lineItemFulfillmentStatus", th.StringType),
                    th.Property("listingMarketplaceId", th.StringType),
                    th.Property("purchaseMarketplaceId", th.StringType),
                    th.Property("soldFormat", th.StringType),
                    th.Property(
                        "lineItemCost",
                        amount_schema,
                    ),
                    th.Property(
                        "total",
                        amount_schema,
                    ),
                    th.Property(
                        "deliveryCost",
                        amount_schema,
                    ),
                    th.Property(
                        "taxes",
                        th.ArrayType(
                            th.ObjectType(
                                th.Property("taxType", th.StringType),
                                th.Property(
                                    "amount",
                                    amount_schema,
                                ),
                            )
                        ),
                    ),
                    th.Property(
                        "refunds",
                        th.ArrayType(
                            th.ObjectType(
                                th.Property("refundId", th.StringType),
                                th.Property("refundDate", th.DateTimeType),
                                th.Property(
                                    "amount",
                                    amount_schema,
                                ),
                            )
                        ),
                    ),
                    th.Property(
                        "properties", th.CustomType({"type": ["object", "string"]})
                    ),
                    # inside each lineItem ObjectType
                    th.Property(
                        "lineItemFulfillmentInstructions",
                        th.ObjectType(
                            th.Property("minEstimatedDeliveryDate", th.DateTimeType),
                            th.Property("maxEstimatedDeliveryDate", th.DateTimeType),
                            th.Property("shipByDate", th.DateTimeType),
                            th.Property("guaranteedDelivery", th.BooleanType),
                        ),
                    ),
                    th.Property(
                        "itemLocation",
                        th.ObjectType(
                            th.Property("location", th.StringType),
                            th.Property("countryCode", th.StringType),
                            th.Property("postalCode", th.StringType),
                        ),
                    ),
                )
            ),
        ),
        th.Property(
            "pricingSummary",
            th.ObjectType(
                th.Property("adjustment", amount_schema),
                th.Property("deliveryCost", amount_schema),
                th.Property("deliveryDiscount", amount_schema),
                th.Property("fee", amount_schema),
                th.Property("priceDiscount", amount_schema),
                th.Property("priceSubtotal", amount_schema),
                th.Property("tax", amount_schema),
                th.Property("total", amount_schema),
            ),
        ),
        th.Property(
            "paymentSummary",
            th.ObjectType(
                th.Property(
                    "payments",
                    th.ArrayType(
                        th.ObjectType(
                            th.Property("paymentDate", th.DateTimeType),
                            th.Property("paymentMethod", th.StringType),
                            th.Property("paymentStatus", th.StringType),
                            th.Property("paymentReferenceId", th.StringType),
                            th.Property(
                                "amount",
                                amount_schema,
                            ),
                        )
                    ),
                ),
                th.Property(
                    "refunds",
                    th.ArrayType(
                        th.ObjectType(
                            th.Property("refundReferenceId", th.StringType),
                            th.Property("refundStatus", th.StringType),
                            th.Property("refundDate", th.DateTimeType),
                            th.Property(
                                "amount",
                                amount_schema,
                            ),
                        )
                    ),
                ),
                th.Property("totalDueSeller", amount_schema),
            ),
        ),
        th.Property(
            "fulfillmentStartInstructions",
            th.ArrayType(
                th.ObjectType(
                    th.Property("fulfillmentInstructionsType", th.StringType),
                    th.Property("minEstimatedDeliveryDate", th.DateTimeType),
                    th.Property("maxEstimatedDeliveryDate", th.DateTimeType),
                    th.Property("ebaySupportedFulfillment", th.BooleanType),
                    th.Property(
                        "shippingStep",
                        th.ObjectType(
                            th.Property(
                                "shipTo",
                                th.ObjectType(
                                    th.Property("fullName", th.StringType),
                                    th.Property(
                                        "contactAddress",
                                        th.ObjectType(
                                            th.Property("addressLine1", th.StringType),
                                            th.Property("addressLine2", th.StringType),
                                            th.Property("city", th.StringType),
                                            th.Property(
                                                "stateOrProvince", th.StringType
                                            ),
                                            th.Property("postalCode", th.StringType),
                                            th.Property("countryCode", th.StringType),
                                        ),
                                    ),
                                    th.Property(
                                        "primaryPhone",
                                        th.ObjectType(
                                            th.Property("phoneNumber", th.StringType),
                                        ),
                                    ),
                                ),
                            ),
                            th.Property("shippingCarrierCode", th.StringType),
                            th.Property("shippingServiceCode", th.StringType),
                        ),
                    ),
                )
            ),
        ),
        th.Property(
            "fulfillmentHrefs",
            th.ArrayType(th.StringType),
        ),
        th.Property("salesRecordReference", th.StringType),
        th.Property("totalFeeBasisAmount", amount_schema),
        th.Property("totalMarketplaceFee", amount_schema)
    ).to_dict()
