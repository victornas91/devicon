# pycharm complains that build_assets is an unresolved ref
# don't worry about it, the script still runs
from build_assets.SeleniumRunner import SeleniumRunner
from build_assets import filehandler, arg_getters, util


def main():
    runner = None
    try:
        args = arg_getters.get_selenium_runner_args(True)
        new_icons = filehandler.find_new_icons(args.devicon_json_path, args.icomoon_json_path)

        if len(new_icons) == 0:
            raise Exception("No files need to be uploaded. Ending script...")

        # get only the icon object that has the name matching the pr title
        filtered_icon = util.find_object_added_in_this_pr(new_icons, args.pr_title)
        print("Icon being checked:", filtered_icon, sep = "\n", end='\n\n')

        runner = SeleniumRunner(args.download_path, args.geckodriver_path, args.headless)
        svgs = filehandler.get_svgs_paths([filtered_icon], args.icons_folder_path, True)
        screenshot_folder = filehandler.create_screenshot_folder("./") 
        runner.upload_svgs(svgs, screenshot_folder)
        print("Task completed.")

        # no errors, do this so upload-artifact won't fail
        filehandler.write_to_file("./err_messages.txt", "0")
    except Exception as e:
        filehandler.write_to_file("./err_messages.txt", str(e))
        util.exit_with_err(e)
    finally:
        runner.close() 


if __name__ == "__main__":
    main()
