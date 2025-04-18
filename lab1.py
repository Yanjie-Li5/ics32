import numpy as np
import imageio
import os
import time

def create_darktex(filepath, shadow_color):
    """
    Replicates the Blender shading dark texture logic on a PNG file.
    
    :param filepath: Path to input PNG file.
    :param shadow_color: Dict with 'r', 'g', 'b' float values in 0–1 range.
    """
    if not os.path.isfile(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
    
    filename = os.path.basename(filepath)
    out_dir = os.path.join(os.path.dirname(filepath), 'dark_files')
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, filename.replace('.png', '_DT.png'))

    if os.path.exists(out_path):
        print("Dark version already exists:", out_path)
        return

    ok = time.time()
    # Load image (RGBA)
    image = imageio.imread(filepath).astype(np.float32) / 255.0  # normalize to 0–1
    if image.shape[2] != 4:
        raise ValueError("Image must have 4 channels (RGBA)")

    pixels = image.reshape((-1, 4))
    diffuse = pixels.copy()

    x, y, z, w = 0, 1, 2, 3

    _ShadowColor = np.array([
        shadow_color['r'],
        shadow_color['g'],
        shadow_color['b'],
        1
    ], dtype=np.float32)

    # === Rewriting the Blender shading logic in NumPy ===
    t0 = diffuse
    t1 = t0[:, [y, z, z, x]] * _ShadowColor[[y, z, z, x]]
    t2 = t1[:, [y, x]]
    t3 = t0[:, [y, z]] * _ShadowColor[[y, z]] - t2

    tb30 = t2[:, [1]] >= t1[:, [1]]
    t30 = tb30.astype(np.float32)

    t2 = np.hstack((
        t2[:, [0, 1]],
        np.full((t2.shape[0], 1), -1, dtype=np.float32),
        np.full((t2.shape[0], 1), 0.666666687, dtype=np.float32)
    ))

    t3 = np.hstack((
        t3[:, [0, 1]],
        np.full((t3.shape[0], 1), 1, dtype=np.float32),
        np.full((t3.shape[0], 1), -1, dtype=np.float32)
    ))

    t2 = t30 * t3 + t2

    tb30 = t1[:, [3]] >= t1[:, [0]]
    t30 = tb30.astype(np.float32)

    t1 = np.hstack((t2[:, [0, 1, 3]], t1[:, [3]]))
    t2 = np.hstack((t1[:, [3, 1]], t2[:, [2]], t1[:, [0]]))
    t2 = -t1 + t2
    t1 = t30 * t2 + t1

    t30 = np.minimum(t1[:, [1]], t1[:, [3]])
    t30 = -t30 + t1[:, [0]]
    t2[:, [0]] = t30 * 6 + 1.00000001e-10

    t11 = -t1[:, [1]] + t1[:, [3]]
    t11 = t11 / t2[:, [0]]
    t11 = t11 + t1[:, [2]]
    t1[:, [0]] = t1[:, [0]] + 1.00000001e-10
    t30 = t30 / t1[:, [0]]
    t30 = t30 * 0.5

    t1 = np.abs(t11) + np.array([0.0, -0.333333343, 0.333333343, 1], dtype=np.float32)
    t1 = t1 - np.floor(t1)
    t1 = -t1 * 2 + 1
    t1 = np.abs(t1) * 3 - 1
    t1 = np.clip(t1, 0, 1)
    t1 = t1 - 1
    t1 = t30 * t1 + 1

    shadingAdjustment = t1

    diffuseShaded = shadingAdjustment * 0.899999976 - 0.5
    diffuseShaded = -diffuseShaded * 2 + 1

    compTest = 0.555555582 < shadingAdjustment
    shadingAdjustment *= 1.79999995
    diffuseShaded = -diffuseShaded * 0.7225 + 1

    hlslcc_movcTemp = shadingAdjustment.copy()
    for i in [x, y, z]:
        hlslcc_movcTemp[:, [i]] = np.where(
            compTest[:, [i]],
            diffuseShaded[:, [i]],
            shadingAdjustment[:, [i]]
        )

    shadingAdjustment = np.clip(hlslcc_movcTemp, 0, 1)
    diffuseShadow = diffuse[:, :3] * shadingAdjustment[:, :3]

    ambientCol = np.array([1.0656, 1.0656, 1.0656], dtype=np.float32)
    diffuseShadow *= ambientCol

    final_pixels = np.hstack((diffuseShadow, diffuse[:, [3]]))
    final_image = final_pixels.reshape(image.shape)
    final_image = np.clip(final_image, 0, 1)

    # Save as PNG
    imageio.imwrite(out_path, (final_image * 255).astype(np.uint8))
    print(f"Created dark version of {filename} in {time.time() - ok:.2f}s")
    return out_path


# Example usage
if __name__ == "__main__":
    create_darktex("your_texture.png", {'r': 0.4, 'g': 0.4, 'b': 0.4})
    print("Finish")
