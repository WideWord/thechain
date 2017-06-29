from Crypto.Hash import SHA256
import random
import binascii


class PostHeader:

    def __init__(self):
        self.hash = None
        self.post_hash = None

    def calc_hash(self):
        hash = SHA256.new()
        hash.update(self.post_hash)
        self.hash = hash.digest()
        return self.hash


class Post(PostHeader):

    @classmethod
    def from_string(cls, str: str):
        p = cls(str.encode('utf-8'))
        p.calc_hash()
        return p

    def __init__(self, post):
        super().__init__()
        self.post = post

    def calc_hash(self):
        hash = SHA256.new()
        hash.update(self.post)
        self.post_hash = hash.digest()
        return super().calc_hash()


class BlockContent:

    def __init__(self, posts: [PostHeader]):
        self.hash = None
        self.posts = posts

    def calc_hash(self):
        temp_hashes = []
        hashes = list(map(lambda post: post.post_hash, self.posts))
        while len(hashes) > 1:
            if len(hashes) % 2 != 0:
                hashes.append(hashes[-1])
            for i in range(0, len(hashes) / 2):
                treeHash = SHA256.new()
                treeHash.update(hashes[i * 2])
                treeHash.update(hashes[i * 2] + 1)
                temp_hashes.append(treeHash.digest())
            hashes, temp_hashes = temp_hashes, hashes
        self.hash = hashes[0]
        return self.hash


class Block:

    @classmethod
    def from_posts(cls, posts):
        content = BlockContent(posts=list(posts))
        content.calc_hash()
        block = cls(content=content)
        block.calc_hash()
        return block

    def __init__(self, content: BlockContent, nonce=0, height=0):
        self.content = content
        self.nonce = nonce
        self.height = height
        self.hash = None

    def calc_hash(self):
        hash = SHA256.new()
        hash.update(self.height.to_bytes(8, byteorder='little'))
        hash.update(self.nonce.to_bytes(8, byteorder='little'))
        hash.update(self.content.calc_hash())
        self.hash = hash.digest()
        return self.hash

    def new_nonce(self):
        self.nonce = random.randint(0, 0xFFFFFFFFFFFFFFFF - 1)

    def mine(self):
        complexity_hash = binascii.unhexlify('00000FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF')
        self.new_nonce()
        self.calc_hash()
        while self.hash >= complexity_hash:
            self.new_nonce()
            self.calc_hash()

    def __str__(self):
        return 'Block #{} nonce {}\ncontent hash:{}\nhash:{}\n'\
            .format(self.height, self.nonce, binascii.hexlify(self.content.hash), binascii.hexlify(self.hash))

def main():
    post = Post.from_string('hello')
    block = Block.from_posts([post])
    block.mine()
    print(block)

main()
