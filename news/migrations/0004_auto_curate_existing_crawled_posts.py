from django.db import migrations


def auto_curate_existing_crawled_posts(apps, schema_editor):
    Post = apps.get_model("news", "Post")
    Post.objects.filter(source_type="crawled", is_curated=False).update(is_curated=True)


class Migration(migrations.Migration):

    dependencies = [
        ("news", "0003_add_is_curated"),
    ]

    operations = [
        migrations.RunPython(
            auto_curate_existing_crawled_posts,
            migrations.RunPython.noop,
        ),
    ]
