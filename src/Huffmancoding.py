import heapq
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
        # ✅ الإصلاح ١: كل حرف = 8 بت بغض النظر عن الترميز
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

    # ✅ الإصلاح ٢: iterative بدلاً من recursive
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
        result = []
        node = self.root 
        for bit in encoded_text:
            node = node.left if bit == "0" else node.right
            if node.char is not None:
                result.append(node.char)
                node = self.root
        return "".join(result)

    def display_info(self):
        print(f"Original text: {self.text}")
        print(f"Unique characters: {self.num_of_chars}")
        print(f"Original size: {self.original_bits} bits")
        print(f"Compressed size: {self.compressed_bits} bits")
        print(f"Compression ratio: {self.compressed_bits / self.original_bits:.2f}")
        print("Huffman codes:")
        for char, code in self.codes.items():
            print(f"  '{char}': {code}")

if __name__ == "__main__":
    text = input("Enter text to compress: ")
    if text:
        huff = Huffman(text)
        huff.display_info()
        print(f"Encoded: {huff.encoded_text}")
        decoded = huff.decode(huff.encoded_text)
        print(f"Decoded: {decoded}")
        print("Match:", text == decoded)
    else:
        print("No text entered.")
