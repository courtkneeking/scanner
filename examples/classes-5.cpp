#include <pybind11/pybind11.h> // main pybind11 header
#include <pybind11/stl.h> // required for the magical conversion from python list to std::vector

namespace py = pybind11; //type less

/*
 *  A simple bounding box class
 */
class BoundingBox{
    public:
        /*
         *  Create the bounding box from
         */
        BoundingBox(const int x, const int y, const int width, const int height) :
            x(x), y(y), w(width), h(height){
        }

        /*
         *  Calculate the area of the bounding box
         */
        int get_area() const{
            return w*h;
        }

        /*
         *  Check if a point is inside the bounding box
         */
        bool is_inside(const int px, const int py){
            return px > x && px < x + w && py > y && py < y + h;
        }

    private:
        const int x, y, w, h;
};

// define the bindings between the c++ code to the python names here.
// the object m is the representation of the python module in c++
// the name of the module is "example_functions" in python.
// IT IS EXTREMELY IMPORTANT THAT THE MODULE NAME MATCHES HERE AND IN THE CMAKE FILE
PYBIND11_MODULE(example_class, m){
    //docstring for the module
    m.doc() = "A small example module containing a single class";
    py::class_<BoundingBox>(m, "BoundingBox").
        def(py::init<const int, const int, const int, const int>()).
        def("get_area", &BoundingBox::get_area).
        def("is_inside", &BoundingBox::is_inside);
}
