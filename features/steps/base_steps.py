from lettuce import *
import subprocess
import os
import tempfile
import shutil

def check_output(*popenargs, **kwargs):
    if hasattr(subprocess, 'check_output'):
        return subprocess.check_output(*popenargs, **kwargs)

    if 'stdout' in kwargs:
        raise ValueError('stdout argument not allowed, it will be overridden.')
    process = subprocess.Popen(*popenargs, stdout=subprocess.PIPE, **kwargs)
    output, unused_err = process.communicate()
    retcode = process.poll()
    if retcode:
        cmd = kwargs.get("args")
        if cmd is None:
            cmd = popenargs[0]
        raise subprocess.CalledProcessError(retcode, cmd, output=output)
    return output

@after.all
def cleanup_project_dir(total_results):
    if hasattr(world, 'project_dir'):
        shutil.rmtree(world.project_dir, ignore_errors=True)

    assert not os.path.exists(world.project_dir)


@step("I have a project")
def create_project(step):
    world.project_dir = tempfile.mkdtemp("jasmine-py")


def install_dependency(name, path=None):
    location = path if path else name

    check_output("pip install {0}".format(location), shell=True)


@step("I install the jasmine distribution")
def install_jasmine(step):
    install_dependency('jasmine', path=os.path.abspath(os.getcwd()))
    check_output("cd {0} && printf 'Y\nY\n' | jasmine-install".format(world.project_dir), shell=True)

    with open("{0}/spec/javascripts/test_spec.js".format(world.project_dir), 'w') as f:
        f.writelines("""
describe("Pants", function() {
    it("should prove the truth", function() {
        expect(true).toBeTruthy();
    });
    it("should prove numbers", function() {
        expect(1).toBe(1);
    });
});
""")


@step("When I run the jasmine command")
def run_jasmine(step):
    world.test_output = check_output("cd {0} && jasmine-ci".format(world.project_dir), shell=True)


@step("Then I should see my tests run")
def check_test_run(step):
    assert "2 specs, 0 failed" in world.test_output