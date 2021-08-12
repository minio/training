Follow the instructions on [Getting the AWS SDK for C++ from a package manager](https://docs.aws.amazon.com/sdk-for-cpp/v1/developer-guide/sdk-from-pm.html)

Specifically, you need to install `vcpkg install "aws-sdk-cpp[s3,sts]" --recurse`.

Once `vcpkg` is set up, run the following cmake command in the `/build` directory.

Replace the path `/home/lab/cpp/` with the path to your `vcpkg` installation. This will create all the cmake files. After that you can run `make run_<filename>` to create the binary, then simply execute the binary to run the function.

```shell
cmake .. -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=/home/lab/cpp/vcpkg/packages/ -DCMAKE_TOOLCHAIN_FILE=/home/lab/cpp/vcpkg/scripts/buildsystems/vcpkg.cmake -DCMAKE_INSTALL_PREFIX=/home/lab/cpp/vcpkg/packages/aws-sdk-cpp_x64-linux/share/aws-cpp-sdk-sts/ -DCMAKE_INSTALL_PREFIX=/home/lab/cpp/vcpkg/packages/aws-sdk-cpp_x64-linux/share/aws-cpp-sdk-s3/ -DBUILD_SHARED_LIBS=ON
```

