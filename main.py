from tempfile import TemporaryDirectory
import argparse
import subprocess
from pathlib import Path
import hashlib
import zipfile

from lbptoolspy import compress_dds_lbp, json2lbpfile, pack_to_mod

_TEXCONV_EXE_ARGS = (Path(__file__).parent / 'texconv.exe',)

_BASE_STICKER_PLAN_TEX_HASH = '276ba996590eff0bf98b71a2e0c93e1a61ed8204'
_BASE_STICKER_PLAN_NAME = 'example_title'
_BASE_STICKER_PLAN_DESC = 'example_desc'
_BASE_STICKER_PLAN_USER = 'example_user'
_BASE_STICKER_PLAN_JSON_STR = """
{
  "revision": 626,
  "branch": {
    "id": "LD",
    "revision": 8
  },
  "type": "PLAN",
  "resource": {
    "things": [
      {
        "UID": 5368,
        "planGUID": 32131,
        "parent": null,
        "group": null,
        "PBody": {
          "posVel": [
            0.0,
            0.0,
            0.0
          ],
          "angVel": 0.0,
          "frozen": 0,
          "editingPlayer": null
        },
        "PPos": {
          "thingOfWhichIAmABone": null,
          "animHash": 0,
          "localPosition": {
            "translation": [
              -20009.793,
              2690.402,
              -851.93317
            ],
            "rotation": [
              0.0,
              0.0,
              -2.0605303E-7,
              1.0
            ],
            "scale": [
              1.0,
              1.0,
              1.0
            ]
          },
          "worldPosition": {
            "translation": [
              -20009.793,
              2690.402,
              -851.93317
            ],
            "rotation": [
              0.0,
              0.0,
              -2.0605303E-7,
              1.0
            ],
            "scale": [
              1.0,
              1.0,
              1.0
            ]
          }
        },
        "PGeneratedMesh": {
          "gfxMaterial": {
            "value": 11166,
            "type": "GFX_MATERIAL"
          },
          "bevel": null,
          "uvOffset": [
            0.0,
            0.0,
            0.0,
            0.0
          ],
          "planGUID": null
        },
        "PStickers": {
          "decals": [
            {
              "texture": {
                "value": "276ba996590eff0bf98b71a2e0c93e1a61ed8204",
                "type": "TEXTURE"
              },
              "u": 0.48266804,
              "v": 0.72956276,
              "xvecu": 0.1075199,
              "xvecv": -5.431096E-8,
              "yvecu": -2.579773E-7,
              "yvecv": 0.21504018,
              "color": -21163,
              "type": "STICKER",
              "metadataIndex": -1,
              "numMetadata": 0,
              "placedBy": -1,
              "playModeFrame": 0,
              "scorchMark": false,
              "plan": null
            }
          ],
          "costumeDecals": [
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            []
          ],
          "paintControl": [],
          "eyetoyData": []
        },
        "PShape": {
          "polygon": {
            "vertices": [
              [
                384.0,
                256.0,
                0.0
              ],
              [
                384.0,
                0.0,
                0.0
              ],
              [
                128.0,
                0.0,
                0.0
              ],
              [
                128.0003,
                255.9999,
                0.0
              ]
            ],
            "loops": [
              4
            ]
          },
          "material": {
            "value": 3465,
            "type": "MATERIAL"
          },
          "oldMaterial": null,
          "thickness": 50.0,
          "massDepth": 1.0,
          "color": -11711155,
          "bevelSize": 10.0,
          "interactPlayMode": 0,
          "interactEditMode": 1,
          "lethalType": "NOT",
          "soundEnumOverride": "NONE",
          "flags": 7
        },
        "PGroup": {
          "planDescriptor": null,
          "creator": "",
          "emitter": null,
          "lifetime": 0,
          "aliveFrames": 0,
          "flags": 0
        }
      }
    ],
    "inventoryData": {
      "dateAdded": 0,
      "levelUnlockSlotID": "NONE",
      "highlightSound": null,
      "colour": -1,
      "type": [
        "STICKER",
        "USER_STICKER"
      ],
      "subType": 0,
      "titleKey": 0,
      "descriptionKey": 0,
      "userCreatedDetails": {
        "name": "example_title",
        "description": "example_desc"
      },
      "creationHistory": null,
      "icon": {
        "value": "276ba996590eff0bf98b71a2e0c93e1a61ed8204",
        "type": "TEXTURE"
      },
      "photoData": null,
      "eyetoyData": null,
      "locationIndex": -1,
      "categoryIndex": -1,
      "primaryIndex": 0,
      "lastUsed": 0,
      "numUses": 0,
      "fluffCost": 0,
      "allowEmit": false,
      "shareable": false,
      "copyright": false,
      "creator": "example_user",
      "toolType": "NONE",
      "location": 0,
      "category": 0
    }
  }
}
"""


def get_sha1_hex(data: bytes) -> str:
    m = hashlib.sha1()
    m.update(data)
    return m.hexdigest()


def images_to_lbp_mods(output_mod: Path, input_images: list[Path],/,description: str | None, username: str | None, show_extensions: bool,) -> None:
    if description is None:
        description = ''
    if username is None:
        username = ''

    current_json_base = _BASE_STICKER_PLAN_JSON_STR.replace(_BASE_STICKER_PLAN_DESC,description).replace(_BASE_STICKER_PLAN_USER,username)

    with TemporaryDirectory() as tp_str:
        tp = Path(tp_str)
        mods_folder = tp / 'stickers'
        plans_folder = mods_folder / 'plan_folder'
        texs_folder = mods_folder / 'tex_folder'

        mods_folder.mkdir()
        plans_folder.mkdir()
        texs_folder.mkdir()

        json_file = tp / 'plan.json'

        for image_path in input_images:
            # check if image exists
            image_path.open().close()

            pretty_name = image_path.name if show_extensions else Path(image_path.name).with_suffix('').name
            tex_path = texs_folder / (image_path.name + '.tex')
            plan_path = plans_folder / (image_path.name + '.plan')

            image_path = image_path.resolve()

            test_result = subprocess.run(_TEXCONV_EXE_ARGS + ('-m','0','-f','DXT5',image_path,'-y'),capture_output = True, shell=False, cwd=tp)
            if test_result.returncode or test_result.stderr:
                raise Exception(f'something went wrong with converting the image to dds, code: {test_result.returncode}, {test_result.stdout!r}')


            tex_bytes = compress_dds_lbp(Path(tp,image_path.name).with_suffix('.dds').read_bytes())
            tex_hash = get_sha1_hex(tex_bytes)
            tex_path.write_bytes(tex_bytes)

            json_str = current_json_base.replace(_BASE_STICKER_PLAN_TEX_HASH,tex_hash).replace(_BASE_STICKER_PLAN_NAME,pretty_name)
            json_file.write_text(json_str)

            json2lbpfile(json_file,plan_path)

        with zipfile.ZipFile(output_mod,'w') as f:
            pack_to_mod(mods_folder,f)


def main() -> None:
    parser = argparse.ArgumentParser('Windows only tool to convert images to sticker mod files for Craftworld Toolkit')
    parser.add_argument('output_mod', help='output of finished mod file, eg out.mod', type=Path)
    parser.add_argument('-d', '--description', required=False, help='optional description of the stickers')
    parser.add_argument('-u', '--username', required=False, help='optional set username of the stickers')
    parser.add_argument('-s', '--show-extensions', action='store_true', help='do you want the stickers to include the extensions? eg my_image.png instead of my_image')
    parser.add_argument('-i', '--images', nargs='+', required=True, help='images to convert to a craftworld toolkit mod file', type=Path)
    args = parser.parse_args()

    images_to_lbp_mods(args.output_mod,args.images,args.description,args.username,args.show_extensions)


if __name__ == '__main__':
    main()