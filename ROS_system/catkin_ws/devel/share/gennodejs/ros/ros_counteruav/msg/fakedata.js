// Auto-generated. Do not edit!

// (in-package ros_counteruav.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;

//-----------------------------------------------------------

class fakedata {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.data = null;
      this.num = null;
    }
    else {
      if (initObj.hasOwnProperty('data')) {
        this.data = initObj.data
      }
      else {
        this.data = [];
      }
      if (initObj.hasOwnProperty('num')) {
        this.num = initObj.num
      }
      else {
        this.num = 0;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type fakedata
    // Serialize message field [data]
    bufferOffset = _arraySerializer.uint8(obj.data, buffer, bufferOffset, null);
    // Serialize message field [num]
<<<<<<< Updated upstream
    bufferOffset = _serializer.uint64(obj.num, buffer, bufferOffset);
=======
    bufferOffset = _serializer.uint8(obj.num, buffer, bufferOffset);
>>>>>>> Stashed changes
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type fakedata
    let len;
    let data = new fakedata(null);
    // Deserialize message field [data]
    data.data = _arrayDeserializer.uint8(buffer, bufferOffset, null)
    // Deserialize message field [num]
<<<<<<< Updated upstream
    data.num = _deserializer.uint64(buffer, bufferOffset);
=======
    data.num = _deserializer.uint8(buffer, bufferOffset);
>>>>>>> Stashed changes
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += object.data.length;
<<<<<<< Updated upstream
    return length + 12;
=======
    return length + 5;
>>>>>>> Stashed changes
  }

  static datatype() {
    // Returns string type for a message object
    return 'ros_counteruav/fakedata';
  }

  static md5sum() {
    //Returns md5sum for a message object
<<<<<<< Updated upstream
    return '8a9dfb9a2c533f9dbe4573a54646cd9a';
=======
    return '779cd9dc2f41ba0741e7ebbe961855fd';
>>>>>>> Stashed changes
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    uint8[] data
<<<<<<< Updated upstream
    uint64   num
=======
    uint8 num
>>>>>>> Stashed changes
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new fakedata(null);
    if (msg.data !== undefined) {
      resolved.data = msg.data;
    }
    else {
      resolved.data = []
    }

    if (msg.num !== undefined) {
      resolved.num = msg.num;
    }
    else {
      resolved.num = 0
    }

    return resolved;
    }
};

module.exports = fakedata;
