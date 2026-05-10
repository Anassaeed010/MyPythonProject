import heapq
import os
import sys
from collections import Counter


class HuffmanNode:
    def __init__(self, byte, freq):
        self.byte = byte    # int 0-255، أو None للعقد الداخلية
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq


class Huffman:
    def __init__(self, data):
        self.data = data                    # bytes object
        self.freq = Counter(data)           # {0: 5, 65: 12, ...}
        self.num_of_bytes = len(self.freq)
        self.root = self.build_tree()
        self.codes = {}
        self.build_codes(self.root)
        self.encoded_text = self.encode(data)

        self.original_bits = len(data) * 8
        self.compressed_bits = len(self.encoded_text)

    def build_tree(self):
        pq = [HuffmanNode(byte, freq) for byte, freq in self.freq.items()]
        heapq.heapify(pq)
        while len(pq) > 1:
            left = heapq.heappop(pq)
            right = heapq.heappop(pq)
            merged = HuffmanNode(None, left.freq + right.freq)
            merged.left = left
            merged.right = right
            heapq.heappush(pq, merged)
        return pq[0] if pq else None

    def build_codes(self, root):
        if root is None:
            return
        if root.byte is not None:
            self.codes[root.byte] = "0"
            return
        stack = [(root, "")]
        while stack:
            node, current_code = stack.pop()
            if node.byte is not None:
                self.codes[node.byte] = current_code
                continue
            if node.right is not None:
                stack.append((node.right, current_code + "1"))
            if node.left is not None:
                stack.append((node.left, current_code + "0"))

    def encode(self, data):
        return "".join(self.codes[b] for b in data)

    def decode(self, encoded_text):
        if self.root is None:
            return b""
        if self.root.byte is not None:
            return bytes([self.root.byte] * len(encoded_text))
        result = []
        node = self.root
        for bit in encoded_text:
            node = node.left if bit == "0" else node.right
            if node.byte is not None:
                result.append(node.byte)
                node = self.root
        return bytes(result)

    def display_info(self):
        original_bytes = len(self.data)
        compressed_bytes = self.compressed_bits / 8
        print(f"Original size:     {original_bytes} bytes  ({self.original_bits} bits)")
        print(f"Compressed size:   {compressed_bytes:.1f} bytes  ({self.compressed_bits} bits)")
        print(f"Unique bytes:      {self.num_of_bytes} / 256")
        if self.original_bits > 0:
            ratio = self.compressed_bits / self.original_bits
            saving = (1 - ratio) * 100
            print(f"Compression ratio: {ratio:.2f}  (saved {saving:.1f}%)")
        print("Huffman codes (decimal → hex → code):")
        for byte_val, code in sorted(self.codes.items(), key=lambda x: len(x[1])):
            print(f"  {byte_val:3d} (0x{byte_val:02X}): {code}")


def read_file_bytes(path):
    path = os.path.expanduser(path.strip().strip('"').strip("'"))
    try:
        with open(path, "rb") as f:      # rb = read bytes، بدون أي ترميز
            return f.read()
    except FileNotFoundError:
        print(f"File not found: {path}")
    except Exception as exc:
        print(f"Error reading file: {exc}")
    return None


if __name__ == "__main__":
    if len(sys.argv) > 1:
        data = read_file_bytes(sys.argv[1])
    else:
        print("اختر مصدر البيانات:")
        print("  1) ملف (أي نوع)")
        print("  2) نص مباشر")
        choice = input("اختيارك (1/2): ").strip()

        if choice == "1":
            path = input("أدخل مسار الملف: ")
            data = read_file_bytes(path)
        else:
            print("أدخل النص:")
            text = input()
            data = text.encode("utf-8")   # نحوّل النص لـ bytes

    if data:
        huff = Huffman(data)
        huff.display_info()
        print(f"\nEncoded length: {len(huff.encoded_text)} bits")
        decoded = huff.decode(huff.encoded_text)
        print(f"Decode match:   {data == decoded}")
    else:
        print("لا توجد بيانات للمعالجة.")
