import java.math.BigInteger;
import java.security.SecureRandom;

/**
 * Created by abyss on 2016. 3. 3..
 */
public class Rsa {
    private BigInteger eValue;
    private BigInteger nValue;

    /**
     * @param eValue
     * @param nValue
     */
    public Rsa(String eValue, String nValue) {
        eValue = eValue.toLowerCase();
        nValue = nValue.toLowerCase();

        this.eValue = new BigInteger(eValue, 16);
        this.nValue = new BigInteger(nValue, 16);
    }

    /**
     * encrypt
     *
     * @param text
     * @return
     */
    public String encrypt(String text) {
        BigInteger value = pkcs1pad2(text);
        if (value == null) {
            return null;
        }
        value = value.modPow(this.nValue, this.eValue);
        if (value == null) {
            return null;
        }
        String result = value.toString(16);
        if ((result.length() & 1) == 0) {
            return result;
        } else {
            return "0" + result;
        }
    }

    /**
     * pkcs1pad2
     *
     * @param text
     * @return
     */
    private BigInteger pkcs1pad2(String text) {
        int eLength = (this.eValue.bitLength() + 7) >> 3;
        if (text.length() + 11 > eLength) {
            return null;
        }

        byte[] bytes = new byte[eLength];
        int sLength = text.length() - 1;
        while (sLength >= 0 && eLength > 0) {
            bytes[--eLength] = (byte) text.charAt(sLength--);
        }
        bytes[--eLength] = 0;

        SecureRandom random = null;
        try {
            random = SecureRandom.getInstance("SHA1PRNG");
        } catch (Exception e) {
            return null;
        }

        byte[] temp = new byte[2000];
        while (eLength > 2) {
            temp[0] = 0;
            while (temp[0] == 0) {
                random.nextBytes(temp);
            }
            bytes[--eLength] = temp[0];
        }
        bytes[--eLength] = 2;
        bytes[--eLength] = 0;
        return new BigInteger(bytes);
    }

    public static String getEncpw(String id, String pwd, String sessionKey,String eValue, String nValue) {

        String text = (char) sessionKey.length() + sessionKey;
        if (id != null) {
            text = text + (char) id.length() + id;
        }

        if (pwd != null) {
            text = text + (char) pwd.length() + pwd;
        }
        Rsa rsa = new Rsa(eValue.toLowerCase(), nValue);
        return rsa.encrypt(text);
    }

}
