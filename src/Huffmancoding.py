import heapq
import os
import sys
from collections import Counter


class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq


class Huffman:
    def __init__(self, text):
        self.text = text
        self.freq = Counter(text)
        self.num_of_chars = len(self.freq)
        self.root = self.build_tree()
        self.codes = {}
        self.build_codes(self.root)
        self.encoded_text = self.encode(text)

        self.original_bits = len(text) * 8
        self.compressed_bits = len(self.encoded_text)

    def build_tree(self):
        pq = [HuffmanNode(char, freq) for char, freq in self.freq.items()]
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
        # حالة خاصة: نص من حرف واحد فقط
        if root.char is not None:
            self.codes[root.char] = "0"
            return
        stack = [(root, "")]
        while stack:
            node, current_code = stack.pop()
            if node.char is not None:
                self.codes[node.char] = current_code
                continue
            # نضيف اليمين أولاً حتى يُعالج اليسار أولاً (LIFO)
            if node.right is not None:
                stack.append((node.right, current_code + "1"))
            if node.left is not None:
                stack.append((node.left, current_code + "0"))

    def encode(self, text):
        return "".join(self.codes[char] for char in text)

    def decode(self, encoded_text):
        if self.root is None:
            return ""
        if self.root.char is not None:
            return self.root.char * len(encoded_text)
        result = []
        node = self.root
        for bit in encoded_text:
            node = node.left if bit == "0" else node.right
            if node.char is not None:
                result.append(node.char)
                node = self.root
        return "".join(result)

    def display_info(self):
        print(f"Original text length: {len(self.text)}")
        print(f"Unique characters:    {self.num_of_chars}")
        print(f"Original size:        {self.original_bits} bits")
        print(f"Compressed size:      {self.compressed_bits} bits")
        if self.original_bits > 0:
            ratio = self.compressed_bits / self.original_bits
            saving = (1 - ratio) * 100
            print(f"Compression ratio:    {ratio:.2f}  (saved {saving:.1f}%)")
        print("Huffman codes:")
        for char, code in sorted(self.codes.items(), key=lambda x: len(x[1])):
            printable = repr(char) if char in ("\n", "\t", "\r") else char
            print(f"  '{printable}': {code}")


def read_file_text(path):
    path = os.path.expanduser(path.strip().strip('"').strip("'"))
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"File not found: {path}")
    except UnicodeDecodeError:
        print(f"Unable to decode file as UTF-8: {path}")
    except Exception as exc:
        print(f"Error reading file: {exc}")
    return None


if __name__ == "__main__":
    # ── اختيار المصدر ──────────────────────────────────────────────
    if len(sys.argv) > 1:
        # تم تمرير مسار ملف كـ argument
        text = read_file_text(sys.argv[1])
    else:
        print("اختر مصدر النص:")
        print("  1) ملف (أدخل المسار)")
        print("  2) نص مباشر (أدخل النص)")
        choice = input("اختيارك (1/2): ").strip()

        if choice == "1":
            path = input("أدخل مسار الملف: ")
            text = read_file_text(path)
        else:
            print("أدخل النص (اضغط Enter مرتين للانتهاء):")
            lines = []
            while True:
                line = input()
                if line == "":
                    break
                lines.append(line)
            text = "\n".join(lines)

    # ── التشغيل ────────────────────────────────────────────────────
    if text:
        huff = Huffman(text)
        huff.display_info()
        print(f"\nEncoded length: {len(huff.encoded_text)} bits")
        decoded = huff.decode(huff.encoded_text)
        print(f"Decode match:   {text == decoded}")
    else:
        print("لا يوجد نص للمعالجة.")
