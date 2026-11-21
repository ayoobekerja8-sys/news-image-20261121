import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));

const sourceImage = join(here, 'entry.png');

const destinationFolder = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';

const imageBytes: Buffer = readFileSync(sourceImage);

mkdirSync(destinationFolder, { recursive: true });

writeFileSync(join(destinationFolder, 'entry.png'), imageBytes);
