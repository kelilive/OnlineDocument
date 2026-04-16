# Cryptographic Algorithm Taxonomy

- Classified by Algorithmic Goals (Algorithms may appear in multiple categories)
- Each category includes mathematical foundations
- SM algorithms integrated naturally (Chinese standard)

---

## 1. Asymmetric Encryption Algorithms

**Goal:** Public‑key encryption / key transport
**Math Foundations:**

- Integer factorization (RSA)
- Finite‑field discrete logarithm (ElGamal)
- Elliptic curve discrete logarithm (ECIES, SM2)

**Algorithms:**

- RSA (OAEP, PKCS#1 encryption)
- ElGamal Encryption
- ECIES
- SM2 Encryption (Chinese standard, ECC-based)

---

## 2. Digital Signature Algorithms

**Goal:** Authentication, integrity, non‑repudiation
**Math Foundations:**

- Integer factorization (RSA signatures)
- Finite‑field discrete logarithm (DSA)
- Elliptic curve discrete logarithm (ECDSA, EdDSA, SM2)

**Algorithms:**

- RSA Signatures (PSS, PKCS#1 v1.5)
- DSA
- ECDSA
- Ed25519 / Ed448
- SM2 Signature (Chinese standard)

---

## 3. Key Exchange / Key Agreement Algorithms

**Goal:** Derive shared secrets over insecure channels
**Math Foundations:**

- Finite‑field discrete logarithm (DH, DHIES)
- Elliptic curve discrete logarithm (ECDH, ECMQV, SM2)
- Montgomery curves (X25519, X448)

**Algorithms:**

- Diffie–Hellman (DH)
- DHIES
- ECDH
- ECMQV
- X25519 / X448
- SM2 Key Exchange (Chinese standard)

---

## 4. Symmetric Block Ciphers

**Goal:** Confidentiality via fixed‑size block encryption
**Math Foundations:**

- Substitution–permutation networks (AES, Camellia)
- Feistel networks (DES, Blowfish, Twofish, SM4)

**Algorithms:**

- AES (CBC, GCM, CTR, CFB, OFB)
- DES / 3DES
- Camellia
- Twofish
- Blowfish
- IDEA
- SM4 (Chinese standard)

---

## 5. Symmetric Stream Ciphers

**Goal:** High‑speed stream encryption
**Math Foundations:**

- LFSR-based designs
- ARX constructions (Add–Rotate–XOR)

**Algorithms:**

- RC4
- Salsa20
- ChaCha20
- HC‑128 / HC‑256
- Grain family

---

## 6. Cryptographic Hash Functions

**Goal:** One‑way mapping, integrity, fingerprinting
**Math Foundations:**

- Merkle–Damgård (SHA‑1, SHA‑2, MD5, RIPEMD)
- Sponge construction (SHA‑3 / Keccak)

**Algorithms:**

- SHA‑1
- SHA‑2 (SHA‑256 / SHA‑512)
- SHA‑3 (Keccak)
- MD5
- RIPEMD160
- Whirlpool
- SM3 (Chinese standard)

---

## 7. Message Authentication Codes (MAC)

**Goal:** Integrity + authenticity with shared key
**Math Foundations:**

- Hash‑based MAC (HMAC)
- Block‑cipher‑based MAC (CMAC, GMAC)

**Algorithms:**

- HMAC (SHA‑1 / SHA‑2 / SHA‑3 / SM3)
- CMAC (AES, SM4)
- GMAC (GCM authentication)

---

## 8. Key Derivation Functions (KDF)

**Goal:** Derive strong keys from passwords or shared secrets
**Math Foundations:**

- Iterated hashing
- HMAC‑based PRF
- Memory‑hard functions

**Algorithms:**

- PBKDF2
- HKDF
- KDF1 / KDF2
- Scrypt

---

## 9. Random Number Generators (RNG / DRBG)

**Goal:** Generate cryptographically secure random values
**Math Foundations:**

- Entropy extraction
- Hash‑DRBG
- HMAC‑DRBG
- CTR‑DRBG

**Mechanisms:**

- SecureRandom
- SP800‑90A DRBG family

---

## Notes

- Algorithms may appear in multiple categories (e.g., RSA, SM2).
- SM algorithms are integrated into their natural categories with a simple "(Chinese standard)" tag.
- This taxonomy reflects real cryptographic usage rather than forcing uniqueness.
