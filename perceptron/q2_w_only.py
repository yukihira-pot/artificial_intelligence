import numpy as np

x1 = np.array([0, 0, 1, 1])
x2 = np.array([0, 1, 0, 1])
x3 = np.array([1, 1, 1, 1])
y_asts = np.array([-1, 1, 1, -1])

w = np.array([0, 0, 0])

success_count = 0
for i in range(3 * len(x1)):
    j = i % 4
    if i % 4 == 0:
        print(f"【 {i // 4 + 1} エポック目】")
    
    w_out = "[" + " ".join([str(i) for i in list(w)]) + "]"
    # print(f"1. 重みは {w_out} である。データセットの {j + 1} 番目を用いる。")

    f = np.array([x1[j], x2[j], x3[j]])
    f_out = "[" + " ".join([str(i) for i in list(f)]) + "]"
    # print(f"2. f = [ (現在の x_1), (現在の x_2), 1 ] であるから、{f} である。")
    y = 1 if np.dot(w.T, f) >= 0 else -1
    y_ast = y_asts[j]
    # print(f"3. <w, f(x)> = {np.dot(w.T, f)} なので、y = {y}。また、y* = {y_ast}。")

    w_out = "[" + " ".join([str(i) for i in list(w)]) + "]"
    if y != y_ast:
        w += np.dot(y_ast.T, f)
        # print(f"4. y ≠ y* より、w = w + <y*, f> として、w は {w_out} となる。")
        success_count = 0
    else:
        # print("4. y = y* より、w の更新は行わない。")
        success_count += 1

    print(w_out)

    if success_count == 4:
        print("データセットを 1 周しても重みが更新されなかったため、ここで計算を打ち切る。")
        break