import shutil
from pathlib import Path

if __name__ == "__main__":
    from project_root import DATA_ROOT

    CPG_root_dir = DATA_ROOT / "cellpose_generalized"
    CPS_root_dir = DATA_ROOT / "cellpose_specialized"

    if not (CPG_root_dir).exists():
        raise ValueError("cellpose_generalized not exists, please run CPG.py first.")

    CPS_root_dir.mkdir(exist_ok=True)
    (CPS_root_dir / "train").mkdir(exist_ok=True)
    (CPS_root_dir / "train" / "images").mkdir(exist_ok=True)
    (CPS_root_dir / "train" / "masks").mkdir(exist_ok=True)
    (CPS_root_dir / "test").mkdir(exist_ok=True)
    (CPS_root_dir / "test" / "images").mkdir(exist_ok=True)
    (CPS_root_dir / "test" / "masks").mkdir(exist_ok=True)

    train_images = sorted(list(Path(CPG_root_dir / "train" / "images").glob("*_img.png")))[:89]
    train_masks = sorted(list(Path(CPG_root_dir / "train" / "masks").glob("*_masks.png")))[:89]
    for img, mask in zip(train_images, train_masks):
        shutil.copy(img, CPS_root_dir / "train" / "images" / img.name)
        shutil.copy(mask, CPS_root_dir / "train" / "masks" / mask.name)

    test_images = sorted(list(Path(CPG_root_dir / "test" / "images").glob("*_img.png")))[:11]
    test_masks = sorted(list(Path(CPG_root_dir / "test" / "masks").glob("*_masks.png")))[:11]
    for img, mask in zip(test_images, test_masks):
        shutil.copy(img, CPS_root_dir / "test" / "images" / img.name)
        shutil.copy(mask, CPS_root_dir / "test" / "masks" / mask.name)