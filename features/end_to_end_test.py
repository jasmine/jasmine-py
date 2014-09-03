import subprocess
import os

def test_end_to_end(tmpdir):
    install_jasmine(tmpdir)
    output = run_jasmine(tmpdir)
    assert "2 specs, 0 failed" in str(output)

def install_dependency(name, path=None):
    location = path if path else name
    check_output("pip install {0}".format(location), shell=True)


def install_jasmine(project_dir):
    install_dependency('jasmine', path=os.path.abspath(os.getcwd()))
    check_output("cd {0} && printf 'Y\nY\n' | jasmine-install".format(project_dir), shell=True)

    with open("{0}/spec/javascripts/test_spec.js".format(project_dir), 'w') as f:
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


def run_jasmine(project_dir):
    return check_output("cd {0} && jasmine-ci".format(project_dir), shell=True)


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