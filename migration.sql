BEGIN;

-- Drop unwanted tables if they exist
DROP TABLE IF EXISTS training_learning_objectives CASCADE;
DROP TABLE IF EXISTS training_prerequisites CASCADE;
DROP TABLE IF EXISTS training_modules CASCADE;
DROP TABLE IF EXISTS training_materials_tags CASCADE;
DROP TABLE IF EXISTS training_tags CASCADE;
DROP TABLE IF EXISTS training_categories CASCADE;

-- Drop unwanted columns from training_materials
ALTER TABLE training_materials
DROP COLUMN IF EXISTS description,
DROP COLUMN IF EXISTS category_id,
DROP COLUMN IF EXISTS difficulty,
DROP COLUMN IF EXISTS estimated_duration,
DROP COLUMN IF EXISTS instructor,
DROP COLUMN IF EXISTS thumbnail_image,
DROP COLUMN IF EXISTS cover_image,
DROP COLUMN IF EXISTS video_url,
DROP COLUMN IF EXISTS document_url,
DROP COLUMN IF EXISTS github_url,
DROP COLUMN IF EXISTS external_link,
DROP COLUMN IF EXISTS featured;

COMMIT;
