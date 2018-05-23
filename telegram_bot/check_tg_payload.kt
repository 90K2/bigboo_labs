
private val HEX_CHARS = "0123456789ABCDEF".toCharArray()

fun ByteArray.toHex() : String{
    val result = StringBuffer()

    forEach {
        val octet = it.toInt()
        val firstIndex = (octet and 0xF0).ushr(4)
        val secondIndex = octet and 0x0F
        result.append(HEX_CHARS[firstIndex])
        result.append(HEX_CHARS[secondIndex])
    }
    return result.toString()
}

fun String.sha256(): ByteArray {
    return this.hashWithAlgorithm("SHA-256")
}

private fun String.hashWithAlgorithm(algorithm: String): ByteArray {
    val digest = MessageDigest.getInstance(algorithm)
    return digest.digest(this.toByteArray(Charsets.UTF_8))
}

object HashUtils {
    fun createHmac(data: ByteArray, key: ByteArray): ByteArray {
        val keySpec = SecretKeySpec(key, "HmacSHA256")
        val mac = Mac.getInstance("HmacSHA256")
        mac.init(keySpec)
        val hmac = mac.doFinal(data)
        return hmac
    }
}

private fun verifyTelegramHash( tgPayloadDto: MutableMap<String, Any?>, originalHash: String): Boolean {
        val secret_key = BOT_TOKEN.sha256()
        val data_ = mutableListOf<String>()
        for ((key, value) in tgPayloadDto) {
            if (value != null) {
                data_.add("$key=$value")
            }
        }
        data_.sort()
        val data_check_string = data_.joinToString(separator = "\n")
        val calculatedHash = HashUtils.createHmac(data = data_check_string.toByteArray(), key = secret_key).toHex().toLowerCase()
        return calculatedHash == originalHash
    }

// val payloadDict = mutableMapOf(
//             "first_name" to payload!!.first_name,
//             "last_name" to payload.last_name,
//             "id" to payload.id,
//             "photo_url" to payload.photo_url,
//             "username" to payload.username,
//             "auth_date" to payload.auth_date
//     )

// verifyTelegramHash(payloadDict, payload.hash.toString())