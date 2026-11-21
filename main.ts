import { createHash } from 'node:crypto';
import { mkdir, readFile, copyFile, stat } from 'node:fs/promises';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const source = join(dirname(fileURLToPath(import.meta.url)), 'entry.png');
const outputDir = '/output';
const destination = join(outputDir, 'entry.png');
const digest = (bytes) => createHash('sha256').update(bytes).digest('hex');

await mkdir(outputDir, { recursive: true });
const sourceBytes = await readFile(source);
await copyFile(source, destination);
const [sourceStat, outputStat, outputBytes] = await Promise.all([
  stat(source), stat(destination), readFile(destination),
]);
if (sourceStat.size !== outputStat.size || outputStat.size > 1048576 ||
    digest(sourceBytes) !== digest(outputBytes)) {
  throw new Error('entry.png copy failed size or SHA-256 verification');
}
