<html>

<head>
    <link rel="stylesheet" href="https://pyscript.net/alpha/pyscript.css&quot; />
    <script defer src="https://pyscript.net/alpha/pyscript.js"></script&gt;
</head>

<body>
    <py-script>
print("Let's compute π:")
def wallis(n):
    pi = 2
    for i in range(1, n):
        pi *= 4 * i ** 2 / (4 * i ** 2 – 1)
    return pi

pi = wallis(100000)
s = f"π is approximately {pi:.3f}"
print(s)
    </py-script>
</body>

</html>
