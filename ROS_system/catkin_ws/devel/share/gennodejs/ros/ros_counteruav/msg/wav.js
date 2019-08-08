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

class wav {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.wavdata = null;
      this.time = null;
    }
    else {
      if (initObj.hasOwnProperty('wavdata')) {
        this.wavdata = initObj.wavdata
      }
      else {
        this.wavdata = [];
      }
      if (initObj.hasOwnProperty('time')) {
        this.time = initObj.time
      }
      else {
        this.time = 0;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type wav
    // Serialize message field [wavdata]
    bufferOffset = _arraySerializer.float32(obj.wavdata, buffer, bufferOffset, null);
    // Serialize message field [time]
    bufferOffset = _serializer.int32(obj.time, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type wav
    let len;
    let data = new wav(null);
    // Deserialize message field [wavdata]
    data.wavdata = _arrayDeserializer.float32(buffer, bufferOffset, null)
    // Deserialize message field [time]
    data.time = _deserializer.int32(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += 4 * object.wavdata.length;
    return length + 8;
  }

  static datatype() {
    // Returns string type for a message object
    return 'ros_counteruav/wav';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '9c745b9bbbbcdca306399d485d1fa8c2';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    float32[] wavdata
    int32 time
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new wav(null);
    if (msg.wavdata !== undefined) {
      resolved.wavdata = msg.wavdata;
    }
    else {
      resolved.wavdata = []
    }

    if (msg.time !== undefined) {
      resolved.time = msg.time;
    }
    else {
      resolved.time = 0
    }

    return resolved;
    }
};

module.exports = wav;
